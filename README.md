NcrYptor — Secure File Encryption Tool

A desktop GUI application for encrypting and decrypting files using AES-256 CBC encryption with PBKDF2 key derivation. Built for users who want military-grade file security without needing any technical knowledge — encrypt any file in under 3 clicks.


Features


AES-256 CBC encryption — industry-standard symmetric encryption used by governments and enterprises worldwide
PBKDF2 key derivation — your password is never used directly; it's stretched with 100,000 iterations of PBKDF2-HMAC-SHA256 making brute-force attacks computationally infeasible
Random salt + IV — unique salt and initialization vector generated per file; encrypting the same file twice produces different ciphertext
100+ file types supported — works on any file: documents, images, videos, archives, source code, databases
Zero configuration — no account, no internet connection, no dependencies to install beyond running the app
Intuitive GUI — built with Tkinter; designed so non-technical users can operate it without reading a manual



Tech Stack

LayerTechnologyLanguagePython 3.10+GUITkinterEncryptionPyCryptodome (AES-256 CBC)Key DerivationPBKDF2-HMAC-SHA256
