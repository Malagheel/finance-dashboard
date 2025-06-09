BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "accounts" (
	"id"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "categories" (
	"id"	TEXT,
	"name"	TEXT,
	"type"	TEXT CHECK("type" IN ('income', 'expense')),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "transactions" (
	"id"	INTEGER,
	"account_id"	TEXT,
	"category_id"	TEXT,
	"amount"	REAL,
	"date"	TEXT,
	"note"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("account_id") REFERENCES "accounts"("id"),
	FOREIGN KEY("category_id") REFERENCES "categories"("id")
);
INSERT INTO "accounts" VALUES ('A1001','Checking Account');
INSERT INTO "accounts" VALUES ('A1002','Credit Card');
INSERT INTO "categories" VALUES ('C1001','Salary','income');
INSERT INTO "categories" VALUES ('C1002','Groceries','expense');
INSERT INTO "categories" VALUES ('C1003','Rent','expense');
INSERT INTO "categories" VALUES ('C1004','Investments','income');
INSERT INTO "transactions" VALUES (1,'A1001','C1001',3000.0,'2025-05-01','Monthly salary');
INSERT INTO "transactions" VALUES (2,'A1001','C1002',200.0,'2025-05-02','Grocery store');
INSERT INTO "transactions" VALUES (3,'A1001','C1003',1000.0,'2025-05-03','May rent');
INSERT INTO "transactions" VALUES (4,'A1002','C1002',150.0,'2025-05-05','Snacks');
INSERT INTO "transactions" VALUES (5,'A1001','C1004',500.0,'2025-05-10','Stocks');
COMMIT;
