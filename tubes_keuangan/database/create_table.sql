CREATE TABLE users (
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE kategori (
    id_kategori SERIAL PRIMARY KEY,
    nama_kategori VARCHAR(50) NOT NULL
);

CREATE TABLE pemasukan (
    pemasukan_id SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    tanggal DATE,
    jumlah INT NOT NULL,
    deskripsi VARCHAR(50),
    id_kategori INT,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_kategori) REFERENCES kategori(id_kategori)
);

CREATE TABLE pengeluaran (
    pengeluaran_id SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    tanggal DATE,
    jumlah INT NOT NULL,
    deskripsi VARCHAR(50),
    id_kategori INT,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_kategori) REFERENCES kategori(id_kategori)
);

CREATE TABLE anggaran (
    anggaran_id SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    jumlah_anggaran INT NOT NULL,
    periode DATE,
    id_kategori INT,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_kategori) REFERENCES kategori(id_kategori)
);