CREATE OR REPLACE FUNCTION insert_notifyer_client()
RETURNS TRIGGER AS $$
DECLARE
    new_id INTEGER;
BEGIN
    -- Получаем количество элементов в таблице notifyer_clients
    SELECT COUNT(*) INTO new_id FROM notifyer_clients;

    -- Вставляем новую запись в таблицу notifyer_clients
    INSERT INTO notifyer_clients (id, destination_id, schedule_change, source)
    VALUES (new_id, NEW.id, true, 'tg');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_notifyer_client_trigger
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION insert_notifyer_client();
