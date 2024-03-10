CREATE TABLE IF NOT EXISTS labequipment (
    CategoryID SERIAL,
    EquipmentClass varchar, /* Tool, Accessory, ...? */
    Course varchar,
    PRIMARY KEY (CategoryID)
)