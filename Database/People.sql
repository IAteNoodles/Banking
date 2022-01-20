Use Bank;
CREATE TABLE `People`(  
    `ID` VARCHAR(64) NOT NULL PRIMARY KEY COMMENT 'Primary Key (SHA256 of UUID)',
    `FirstName` VARCHAR(20) NOT NULL COMMENT 'Name',
    `MiddleName` VARCHAR(20) NOT NULL COMMENT 'Name',
    `LastName` VARCHAR(20) NOT NULL COMMENT 'Name',
    `DateOfBirth` DATETIME NOT NULL COMMENT 'Date of birth',
    `Address` VARCHAR(50) NOT NULL COMMENT 'Address',
    `Phone` VARCHAR(10) NOT NULL COMMENT 'Phone Number',
    `Email` VARCHAR(50) NOT NULL COMMENT 'Email',
    `PublicKey` BLOB NOT NULL COMMENT 'Public Key. The Private Key will be encrypted with a password, and will be stored in the environment.'
) DEFAULT CHARSET UTF8 COMMENT '';