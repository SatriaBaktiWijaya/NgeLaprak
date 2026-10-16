package com.praktikum.adpl;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Class KoneksiDB — Modul 4 ADPL / PBO
 * Mengatur koneksi terpusat ke database MySQL via JDBC Driver.
 */
public class KoneksiDB {
    private static Connection koneksi;

    public static Connection getKoneksi() {
        if (koneksi == null) {
            try {
                String url = "jdbc:mysql://localhost:3306/db_kasir";
                String user = "root";
                String pass = "";
                DriverManager.registerDriver(new com.mysql.cj.jdbc.Driver());
                koneksi = DriverManager.getConnection(url, user, pass);
                System.out.println("[Sukses] Koneksi Database Berhasil Diinisialisasi!");
            } catch (SQLException e) {
                System.err.println("[Error] Gagal terhubung ke Database: " + e.getMessage());
            }
        }
        return koneksi;
    }
}
