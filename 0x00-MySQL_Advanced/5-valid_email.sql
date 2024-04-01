-- A SQL script that creates a trigger that resets
-- the attribute valid_email only when it has been changed
DROP TRIGGER IF EXISTS validate_mail;
DELIMTER $$
CREATE TRIGGER validate_mail
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END$$
DELIMITER ;
