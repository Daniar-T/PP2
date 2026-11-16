CREATE OR REPLACE PROCEDURE insert_user(
    p_name  TEXT,
    p_phone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts
        WHERE first_name = p_name
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE first_name = p_name;
    ELSE
        INSERT INTO contacts (first_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_users(
    p_names     TEXT[],
    p_phones    TEXT[],
    INOUT p_incorrect TEXT[] DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    i       INTEGER;
    v_count INTEGER;
BEGIN
    p_incorrect := ARRAY[]::TEXT[];

    v_count := LEAST(
        COALESCE(array_length(p_names, 1), 0),
        COALESCE(array_length(p_phones, 1), 0)
    );

    FOR i IN 1 .. v_count LOOP
        IF p_names[i] IS NULL OR btrim(p_names[i]) = ''
           OR p_phones[i] IS NULL OR btrim(p_phones[i]) = '' THEN
            p_incorrect := p_incorrect || ('row ' || i || ': "' ||
                            COALESCE(p_names[i], '') || '" / "' ||
                            COALESCE(p_phones[i], '') || '"');
        ELSE
            INSERT INTO contacts (first_name, phone)
            VALUES (btrim(p_names[i]), btrim(p_phones[i]));
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_user(
    p_name  TEXT DEFAULT NULL,
    p_phone TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_name IS NOT NULL AND btrim(p_name) <> '' THEN
        DELETE FROM contacts WHERE first_name = btrim(p_name);
    ELSIF p_phone IS NOT NULL AND btrim(p_phone) <> '' THEN
        DELETE FROM contacts WHERE phone = btrim(p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    IF p_contact_name IS NULL OR btrim(p_contact_name) = '' THEN
        RAISE EXCEPTION 'Contact name cannot be empty';
    END IF;

    IF p_phone IS NULL OR btrim(p_phone) = '' THEN
        RAISE EXCEPTION 'Phone cannot be empty';
    END IF;

    p_type := lower(coalesce(btrim(p_type), ''));
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION
            'Invalid phone type "%", expected home, work or mobile', p_type;
    END IF;

    SELECT id INTO v_contact_id
    FROM contacts
    WHERE first_name = btrim(p_contact_name)
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    IF EXISTS (
        SELECT 1 FROM phones
        WHERE contact_id = v_contact_id
          AND phone = btrim(p_phone)
    ) THEN
        RAISE NOTICE 'Phone % already exists for contact %',
                     p_phone, p_contact_name;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, btrim(p_phone), p_type);

    RAISE NOTICE 'Phone % (%) added to contact "%"',
                 p_phone, p_type, p_contact_name;
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
    v_moved    INTEGER;
BEGIN
    IF p_contact_name IS NULL OR btrim(p_contact_name) = '' THEN
        RAISE EXCEPTION 'Contact name cannot be empty';
    END IF;

    IF p_group_name IS NULL OR btrim(p_group_name) = '' THEN
        RAISE EXCEPTION 'Group name cannot be empty';
    END IF;

    -- the group is created on the fly when it does not exist
    INSERT INTO groups (name)
    VALUES (btrim(p_group_name))
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = btrim(p_group_name);

    UPDATE contacts
    SET group_id = v_group_id
    WHERE first_name = btrim(p_contact_name);

    GET DIAGNOSTICS v_moved = ROW_COUNT;

    IF v_moved = 0 THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    RAISE NOTICE 'Moved % contact(s) named "%" to group "%" ',
                 v_moved, p_contact_name, p_group_name;
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit  INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id         INTEGER,
    first_name TEXT,
    phone      TEXT
)
LANGUAGE SQL
AS $$
    SELECT c.id, c.first_name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
$$;

DROP FUNCTION IF EXISTS search_contacts(TEXT);

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INTEGER,
    first_name TEXT,
    phone      TEXT,
    email      TEXT,
    group_name TEXT,
    phones     TEXT
)
LANGUAGE SQL
AS $$
    SELECT
        c.id,
        c.first_name,
        c.phone,
        c.email,
        g.name AS group_name,
        COALESCE(
            string_agg(p.type || ': ' || p.phone, ', ' ORDER BY p.id),
            '-'
        ) AS phones
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.phone      LIKE  '%' || p_query || '%'
       OR c.email      ILIKE '%' || p_query || '%'
       OR p.phone      LIKE  '%' || p_query || '%'
    GROUP BY c.id, g.name
    ORDER BY c.id;
$$;
