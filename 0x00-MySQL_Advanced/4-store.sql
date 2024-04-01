-- A Sql script that creates a trigger
DROP TRIGGER IF EXISTS decrease_quantity;

CREATE TRIGGER decrease_quantity
    AFTER INSERT ON orders FOR EACH ROW
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = New.item_name;
