SET CLIENT_ENCODING = 'UTF8';
SET CLIENT_MIN_MESSAGES = WARNING;

-- The group-specific email-settings for a member. If there is no
-- entry in this table then one-email-per-post is assumed.
CREATE TABLE email_setting (
    user_id   TEXT  NOT NULL,
    site_id   TEXT  NOT NULL DEFAULT ''::TEXT,
    group_id  TEXT  NOT NULL DEFAULT ''::TEXT,
    setting   TEXT  NOT NULL
);

CREATE UNIQUE INDEX email_setting_pkey 
       ON email_setting 
       USING BTREE(user_id, site_id, group_id);
