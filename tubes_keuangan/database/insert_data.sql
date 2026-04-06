-- USERS
INSERT INTO users (username, password, name) VALUES
('laila','laila123','Laila'),
('kevin','kevin123','Kevin'),
('alexa','alexa123','Alexa'),
('andi','andi123','Andi'),
('siti','siti123','Siti'),
('budi','budi123','Budi'),
('rina','rina123','Rina'),
('dodi','dodi123','Dodi'),
('putri','putri123','Putri'),
('agus','agus123','Agus');

-- KATEGORI
INSERT INTO kategori (nama_kategori) VALUES
('Makan'),
('Transportasi'),
('Internet'),
('Belanja'),
('Freelance'),
('Beasiswa');

-- PEMASUKAN
INSERT INTO pemasukan (id_user, tanggal, jumlah, deskripsi, id_kategori) VALUES
(1,'2026-03-01',2500000,'Orang tua',5),
(2,'2026-03-01',2000000,'Kampus',5),
(3,'2026-03-01',500000,'Part time',5),
(4,'2026-03-01',200000,'Lomba',5),
(5,'2026-03-01',1000000,'Orang tua',5),
(6,'2026-03-01',750000,'Desain',5),
(7,'2026-03-01',2000000,'Kampus',5),
(8,'2026-03-01',1500000,'Orang tua',5),
(9,'2026-03-01',300000,'Lomba',5),
(10,'2026-03-01',900000,'Coding',5);

-- PENGELUARAN
INSERT INTO pengeluaran (id_user, tanggal, jumlah, deskripsi, id_kategori) VALUES
(1,'2026-03-01',150000,'Mingguan',1),
(2,'2026-03-01',75000,'Ojol',2),
(3,'2026-03-01',200000,'Buku Kuliah',4),
(4,'2026-03-01',100000,'Kuota',3),
(5,'2026-03-01',175000,'Bulanan',1),
(6,'2026-03-01',120000,'Harian',1),
(7,'2026-03-01',80000,'Ojol',2),
(8,'2026-03-01',100000,'Kuota',3),
(9,'2026-03-01',250000,'Shopee',4),
(10,'2026-03-01',130000,'Harian',1);

-- ANGGARAN
INSERT INTO anggaran (id_user, jumlah_anggaran, periode, id_kategori) VALUES
(1,1500000,'2026-03-01',1),
(2,800000,'2026-03-01',2),
(3,1200000,'2026-03-01',4),
(4,500000,'2026-03-01',3),
(5,1000000,'2026-03-01',1),
(6,1200000,'2026-03-01',1),
(7,900000,'2026-03-01',2),
(8,600000,'2026-03-01',3),
(9,1500000,'2026-03-01',4),
(10,1100000,'2026-03-01',1);