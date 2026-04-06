SELECT 
    u.name,
    COALESCE(p.total_pemasukan, 0) AS total_pemasukan,
    COALESCE(pg.total_pengeluaran, 0) AS total_pengeluaran,
    COALESCE(a.total_anggaran, 0) AS total_anggaran,
    COALESCE(p.total_pemasukan, 0) - COALESCE(pg.total_pengeluaran, 0) AS saldo,
    COALESCE(a.total_anggaran, 0) - COALESCE(pg.total_pengeluaran, 0) AS sisa_anggaran
FROM users u
LEFT JOIN (
    SELECT id_user, SUM(jumlah) AS total_pemasukan
    FROM pemasukan
    GROUP BY id_user
) p ON u.id_user = p.id_user
LEFT JOIN (
    SELECT id_user, SUM(jumlah) AS total_pengeluaran
    FROM pengeluaran
    GROUP BY id_user
) pg ON u.id_user = pg.id_user
LEFT JOIN (
    SELECT id_user, SUM(jumlah_anggaran) AS total_anggaran
    FROM anggaran
    GROUP BY id_user
) a ON u.id_user = a.id_user;