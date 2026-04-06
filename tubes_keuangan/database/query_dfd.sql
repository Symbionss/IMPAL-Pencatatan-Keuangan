-- TAMBAH PEMASUKAN
INSERT INTO pemasukan (id_user, tanggal, jumlah, deskripsi, id_kategori)
VALUES (1, CURRENT_DATE, 50000, 'Demo', 5);

-- UPDATE PEMASUKAN
UPDATE pemasukan
SET jumlah = 60000
WHERE deskripsi = 'Demo';

-- DELETE PEMASUKAN
DELETE FROM pemasukan
WHERE deskripsi = 'Demo';

-- LIHAT DATA
SELECT * FROM pemasukan;
SELECT * FROM pengeluaran;