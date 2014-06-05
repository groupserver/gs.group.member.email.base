SET CLIENT_ENCODING = 'UTF8';
SET CLIENT_MIN_MESSAGES = WARNING;

-- The specific email addresses that the group member uses in the
-- group. If the member has no entries in this table then the
-- default email addresses should be used.
CREATE TABLE group_user_email (
    user_id   TEXT  NOT NULL,
    site_id   TEXT  NOT NULL DEFAULT ''::TEXT,
    group_id  TEXT  NOT NULL,
    email     TEXT  NOT NULL REFERENCES user_email(email) ON DELETE CASCADE ON UPDATE CASCADE
);
-- Note the lowered email-address is used in the index
CREATE UNIQUE INDEX user_site_group_email_pkey 
       ON group_user_email 
       USING BTREE (user_id, site_id, group_id, lower(email));
