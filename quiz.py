import asyncio
import random
import time
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message
from aiogram import types, F
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import asyncio
from aiogram import Router, F, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()
dp = Dispatcher()
dp.include_router(router)

# BotFather tomonidan berilgan token
TOKEN = "7518058064:AAG58UJeCryE1jGIRdryCTR51lqq_OQ7xcA"  # Bu yerga haqiqiy tokenni qo'ying
ADMIN_IDS = [7871012050, 7750409176]  # Admin IDlari

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Test savollari
quizzes = {


  "1": [
    {
      "id": 1,
      "question": "Operatsion tizim nima?",
      "options": [
        "Bu kompyuter o‘yini",
        "Bu kompyuterning elektr ta'minoti",
        "Bu foydalanuvchi va kompyuter o‘rtasidagi vosita",
        "Bu faqat grafik interfeys"
      ],
      "correct": 2
    },
    {
      "id": 2,
      "question": "Multitasking bu —",
      "options": [
        "Bir nechta foydalanuvchi ishlashi",
        "Bir vaqtda bir nechta vazifani bajarish",
        "Faqat bitta ilovani ishlatish",
        "Operatsion tizimni yuklash"
      ],
      "correct": 1
    },
    {
      "id": 3,
      "question": "Qaysi biri operatsion tizim emas?",
      "options": [
        "Windows",
        "Linux",
        "MacOS",
        "MS Word"
      ],
      "correct": 3
    },
    {
      "id": 4,
      "question": "Linux ochiq kodli tizimmi?",
      "options": [
        "Ha",
        "Yo‘q",
        "Faqat serverlar uchun",
        "Faqat grafik interfeysli"
      ],
      "correct": 0
    },
    {
      "id": 5,
      "question": "Operatsion tizimning asosiy vazifasi nima?",
      "options": [
        "Rasmlar chizish",
        "Dastur tuzish",
        "Resurslarni boshqarish",
        "Brauzerda ishlash"
      ],
      "correct": 2
    },
    {
      "id": 6,
      "question": "Windows tizimida fayl kengaytmasi qanday ko‘rinadi?",
      "options": [
        ".doc",
        ".exe",
        ".jpg",
        "Barchasi"
      ],
      "correct": 3
    },
    {
      "id": 7,
      "question": "MacOS qaysi kompaniya tomonidan ishlab chiqilgan?",
      "options": [
        "Microsoft",
        "IBM",
        "Apple",
        "Google"
      ],
      "correct": 2
    },
    {
      "id": 8,
      "question": "Linux distributiviga misol keltiring:",
      "options": [
        "Ubuntu",
        "Windows 10",
        "MacOS Ventura",
        "Android"
      ],
      "correct": 0
    },
    {
      "id": 9,
      "question": "Qaysi dastur BIOSga kirish uchun kerak?",
      "options": [
        "F10/F2 tugmalari",
        "Paint",
        "CMD",
        "Excel"
      ],
      "correct": 0
    },
    {
      "id": 10,
      "question": "Fayl tizimi bu —",
      "options": [
        "Printer qurilmasi",
        "Ma'lumotlarni tashkil qilish usuli",
        "Internet protokoli",
        "Operatsion tizimning GUI qismi"
      ],
      "correct": 1
    },
    {
      "id": 11,
      "question": "NTFS bu —",
      "options": [
        "Video format",
        "Fayl tizimi",
        "Audio format",
        "Yadro turi"
      ],
      "correct": 1
    },
    {
      "id": 12,
      "question": "Operatsion tizimning yadro (kernel)si nima qiladi?",
      "options": [
        "Rasmlarni ko‘rsatadi",
        "Fayllarni siqadi",
        "Aloqalarni va resurslarni boshqaradi",
        "CD diskni aylantiradi"
      ],
      "correct": 2
    },
    {
      "id": 13,
      "question": "Qaysi biri real vaqtda ishlovchi OT emas?",
      "options": [
        "RTOS",
        "Windows XP",
        "QNX",
        "VxWorks"
      ],
      "correct": 1
    },
    {
      "id": 14,
      "question": "Bootloader nima?",
      "options": [
        "Fayl arxivi",
        "Internet brauzer",
        "OTni yuklovchi dastur",
        "Grafik interfeys"
      ],
      "correct": 2
    },
    {
      "id": 15,
      "question": "CLI bu —",
      "options": [
        "Grafik interfeys",
        "Buyruq satri interfeysi",
        "Audio tizimi",
        "Fayl kengaytmasi"
      ],
      "correct": 1
    },
    {
      "id": 16,
      "question": "Qanday fayl kengaytmasi bajariluvchi faylni bildiradi?",
      "options": [
        ".exe",
        ".txt",
        ".mp3",
        ".png"
      ],
      "correct": 0
    },
    {
      "id": 17,
      "question": "Multifoydalanuvchi tizim nima qiladi?",
      "options": [
        "Bitta foydalanuvchiga xizmat qiladi",
        "Bir nechta foydalanuvchiga xizmat qiladi",
        "Foydalanuvchining ruxsatisiz ishlaydi",
        "Faqat serverlarda mavjud"
      ],
      "correct": 1
    },
    {
      "id": 18,
      "question": "Process bu —",
      "options": [
        "Statik fayl",
        "Internet manzili",
        "Ishlayotgan dastur",
        "Driver"
      ],
      "correct": 2
    },
    {
      "id": 19,
      "question": "Driver nima?",
      "options": [
        "Printer",
        "Qattiq disk",
        "Qurilma bilan aloqa qilish dasturi",
        "BIOS paroli"
      ],
      "correct": 2
    },
    {
      "id": 20,
      "question": "Shell bu —",
      "options": [
        "Sistemadagi virus",
        "Foydalanuvchi interfeysi qatlami",
        "Fayl nomi",
        "Kengaytma"
      ],
      "correct": 1
    },
    {
      "id": 21,
      "question": "Interfeys bu —",
      "options": [
        "Kompyuter platasining nomi",
        "Ma'lumotlarni uzatish usuli",
        "Foydalanuvchi bilan tizim o‘rtasidagi aloqa",
        "Kursorning turi"
      ],
      "correct": 2
    },
    {
      "id": 22,
      "question": "Komanda satrida `cd` buyrug‘i nimani anglatadi?",
      "options": [
        "Faylni nusxalash",
        "Diskni tekshirish",
        "Katalogga kirish",
        "Katalogni o‘chirish"
      ],
      "correct": 2
    },
    {
      "id": 23,
      "question": "Operatsion tizimda task manager nima vazifa bajaradi?",
      "options": [
        "Internetga ulanadi",
        "Vazifalarni ko‘rsatadi va boshqaradi",
        "Brauzer o‘rnini bosadi",
        "Printerga bog‘lanadi"
      ],
      "correct": 1
    },
    {
      "id": 24,
      "question": "Qanday OTlar serverlar uchun ishlatiladi?",
      "options": [
        "Ubuntu Server, Windows Server",
        "Windows 7, Windows XP",
        "DOS, MacOS",
        "Android, iOS"
      ],
      "correct": 0
    },
    {
      "id": 25,
      "question": "RAM bu —",
      "options": [
        "Doimiy xotira",
        "Qattiq disk",
        "Operativ xotira",
        "Tashqi qurilma"
      ],
      "correct": 2
    }
  ],

  "2": [
    {
      "id": 26,
      "question": "ROM bu —",
      "options": [
        "Faqat o‘qiladigan xotira",
        "Operativ xotira",
        "Flesh xotira",
        "Qattiq disk"
      ],
      "correct": 0
    },
    {
      "id": 27,
      "question": "Qaysi buyruq katalog yaratadi?",
      "options": [
        "mkdir",
        "cd",
        "dir",
        "rm"
      ],
      "correct": 0
    },
    {
      "id": 28,
      "question": "Linuxda superfoydalanuvchi kim?",
      "options": [
        "root",
        "admin",
        "user",
        "guest"
      ],
      "correct": 0
    },
    {
      "id": 29,
      "question": "Qaysi buyruq katalog ichidagilarni ko‘rsatadi?",
      "options": [
        "ls",
        "rm",
        "cd",
        "mv"
      ],
      "correct": 0
    },
    {
      "id": 30,
      "question": "Swap xotira nima?",
      "options": [
        "Doimiy diskdagi vaqtinchalik xotira",
        "BIOSdagi joy",
        "Grafik karta xotirasi",
        "Fleshka xotirasi"
      ],
      "correct": 0
    },
    {
      "id": 31,
      "question": "Virus nima?",
      "options": [
        "Kompyuter o‘yinlari",
        "Zararkunanda dastur",
        "Grafik interfeys",
        "Fayl kengaytmasi"
      ],
      "correct": 1
    },
    {
      "id": 32,
      "question": "Fayl kengaytmasi qaysi belgidan keyin yoziladi?",
      "options": [
        "nuqta (.)",
        "vergul (,)",
        "chiziq (-)",
        "tugma (#)"
      ],
      "correct": 0
    },
    {
      "id": 33,
      "question": "Qanday OT mobil qurilmalar uchun yaratilgan?",
      "options": [
        "Android",
        "Windows 11",
        "Ubuntu",
        "Debian"
      ],
      "correct": 0
    },
    {
      "id": 34,
      "question": "Qaysi fayl tizimi Linuxda ishlatiladi?",
      "options": [
        "ext4",
        "NTFS",
        "FAT32",
        "exFAT"
      ],
      "correct": 0
    },
    {
      "id": 35,
      "question": "Kompyuterning boshlanishi qanday fayl bilan bog‘liq?",
      "options": [
        "Bootloader",
        "Notepad",
        "Recycle bin",
        "Paint"
      ],
      "correct": 0
    },
    {
      "id": 36,
      "question": "Qaysi biri grafik interfeysli OT?",
      "options": [
        "Windows",
        "DOS",
        "CLI",
        "BIOS"
      ],
      "correct": 0
    },
    {
      "id": 37,
      "question": "Kernel bu —",
      "options": [
        "OT yadrosi",
        "Driver",
        "Kursor",
        "Terminal"
      ],
      "correct": 0
    },
    {
      "id": 38,
      "question": "Driver nima qiladi?",
      "options": [
        "Qurilma bilan aloqa o‘rnatadi",
        "Fayl yaratadi",
        "Web sayt ochadi",
        "Virusni topadi"
      ],
      "correct": 0
    },
    {
      "id": 39,
      "question": "Keng tarqalgan grafik interfeysli Linux distributivi?",
      "options": [
        "Ubuntu",
        "FreeDOS",
        "ReactOS",
        "Solaris"
      ],
      "correct": 0
    },
    {
      "id": 40,
      "question": "Kompyuterni o‘chirish buyrug‘i qaysi?",
      "options": [
        "shutdown",
        "cd",
        "dir",
        "ls"
      ],
      "correct": 0
    },
    {
      "id": 41,
      "question": "Terminal bu —",
      "options": [
        "Buyruq kiritish oynasi",
        "Grafik interfeys",
        "Brauzer",
        "Uskuna"
      ],
      "correct": 0
    },
    {
      "id": 42,
      "question": "OS orqali resurslar nima?",
      "options": [
        "Protsessor, xotira, disk",
        "YouTube, Telegram",
        "Printer, telefon",
        "Kameralar"
      ],
      "correct": 0
    },
    {
      "id": 43,
      "question": "Qaysi OS to‘liq ochiq kodli?",
      "options": [
        "Linux",
        "Windows",
        "MacOS",
        "iOS"
      ],
      "correct": 0
    },
    {
      "id": 44,
      "question": "Barcha fayllarni o‘chirish buyrug‘i?",
      "options": [
        "rm -rf",
        "mkdir",
        "cd ..",
        "ls -a"
      ],
      "correct": 0
    },
    {
      "id": 45,
      "question": "Qaysi OS asosan serverlar uchun ishlatiladi?",
      "options": [
        "Ubuntu Server",
        "Windows XP",
        "MacOS",
        "iOS"
      ],
      "correct": 0
    },
    {
      "id": 46,
      "question": "Operatsion tizimdagi GUI nima?",
      "options": [
        "Grafik foydalanuvchi interfeysi",
        "Buyruq satri",
        "BIOS menyusi",
        "Driver sozlamasi"
      ],
      "correct": 0
    },
    {
      "id": 47,
      "question": "Linuxda fayl o‘chirish buyrug‘i?",
      "options": [
        "rm",
        "mv",
        "ls",
        "cd"
      ],
      "correct": 0
    },
    {
      "id": 48,
      "question": "Linuxda fayl ko‘chirish buyrug‘i?",
      "options": [
        "mv",
        "rm",
        "ls",
        "mkdir"
      ],
      "correct": 0
    },
    {
      "id": 49,
      "question": "Zararkunanda dastur qanday nomlanadi?",
      "options": [
        "Malware",
        "Software",
        "Hardware",
        "Freeware"
      ],
      "correct": 0
    },
    {
      "id": 50,
      "question": "FAT32 nima?",
      "options": [
        "Fayl tizimi",
        "Audio format",
        "Grafik drayver",
        "BIOS turi"
      ],
      "correct": 0
    }
  ],

  "3": [
    {
      "id": 51,
      "question": "Windows OT ning oxirgi versiyalaridan biri qaysi?",
      "options": ["Windows 11", "Windows XP", "Windows 7", "Windows 98"],
      "correct": 0
    },
    {
      "id": 52,
      "question": "MacOS asosan qaysi qurilmada ishlatiladi?",
      "options": ["Apple kompyuterlarida", "Android telefonlarida", "Windows noutbuklarda", "Linux serverlarda"],
      "correct": 0
    },
    {
      "id": 53,
      "question": "Linuxda foydalanuvchi huquqlarini ko‘rish buyrug‘i?",
      "options": ["ls -l", "chmod", "pwd", "cd"],
      "correct": 0
    },
    {
      "id": 54,
      "question": "Linuxda huquqlarni o‘zgartirish buyrug‘i?",
      "options": ["chmod", "ls", "mv", "cat"],
      "correct": 0
    },
    {
      "id": 55,
      "question": "Windowsda fayl nomlari maksimal uzunligi?",
      "options": ["255 belgigacha", "128 belgigacha", "64 belgigacha", "100 belgigacha"],
      "correct": 0
    },
    {
      "id": 56,
      "question": "BIOS nima?",
      "options": ["Tizimni ishga tushiruvchi dastur", "Grafik interfeys", "Fayl tizimi", "Drayver"],
      "correct": 0
    },
    {
      "id": 57,
      "question": "Linuxda joriy katalogni ko‘rsatish buyrug‘i?",
      "options": ["pwd", "cd", "ls", "mv"],
      "correct": 0
    },
    {
      "id": 58,
      "question": "Qaysi operatsion tizim real vaqtda ishlovchi hisoblanadi?",
      "options": ["RTOS", "MS-DOS", "Windows 10", "Android"],
      "correct": 0
    },
    {
      "id": 59,
      "question": "Linuxning asosiy yadrosi nima?",
      "options": ["Kernel", "Shell", "Bash", "BIOS"],
      "correct": 0
    },
    {
      "id": 60,
      "question": "Qaysi tizimda `task manager` mavjud?",
      "options": ["Windows", "Linux CLI", "BIOS", "FreeDOS"],
      "correct": 0
    },
    {
      "id": 61,
      "question": "NTFS fayl tizimi qaysi OTda ishlatiladi?",
      "options": ["Windows", "Linux", "MacOS", "Android"],
      "correct": 0
    },
    {
      "id": 62,
      "question": "Linuxda fayl tarkibini ko‘rish buyrug‘i?",
      "options": ["cat", "ls", "rm", "touch"],
      "correct": 0
    },
    {
      "id": 63,
      "question": "OT nima qiladi?",
      "options": ["Resurslarni boshqaradi", "Foydalanuvchiga SMS yuboradi", "Vebsayt tuzadi", "Protsessorni almashtiradi"],
      "correct": 0
    },
    {
      "id": 64,
      "question": "Kompyuterda vaqtincha fayllar qayerda saqlanadi?",
      "options": ["Temp papkada", "C:\\Windows\\System32", "D:\\Program Files", "BIOS ichida"],
      "correct": 0
    },
    {
      "id": 65,
      "question": "Qaysi buyrug‘ orqali fayl yaratiladi?",
      "options": ["touch", "ls", "mv", "rm"],
      "correct": 0
    },
    {
      "id": 66,
      "question": "Android qanday OTga asoslangan?",
      "options": ["Linux", "Windows", "MacOS", "FreeBSD"],
      "correct": 0
    },
    {
      "id": 67,
      "question": "Linuxda katalog yaratish buyrug‘i?",
      "options": ["mkdir", "rmdir", "touch", "cd"],
      "correct": 0
    },
    {
      "id": 68,
      "question": "Faylni boshqa nom bilan saqlash buyrug‘i?",
      "options": ["mv", "cp", "ls", "rm"],
      "correct": 0
    },
    {
      "id": 69,
      "question": "Protsessorni to‘liq ishlatadigan dasturlar qanday ataladi?",
      "options": ["CPU-intensive", "User-level", "Low-power", "Silent-process"],
      "correct": 0
    },
    {
      "id": 70,
      "question": "Linuxda katalogni o‘chirish buyrug‘i?",
      "options": ["rmdir", "rm", "del", "erase"],
      "correct": 0
    },
    {
      "id": 71,
      "question": "Kompyuterga OT o‘rnatish jarayoni nima deb ataladi?",
      "options": ["Install", "Format", "Update", "Load"],
      "correct": 0
    },
    {
      "id": 72,
      "question": "Qaysi tizim serverlar uchun eng mos?",
      "options": ["Linux", "Windows 7", "MacOS", "iOS"],
      "correct": 0
    },
    {
      "id": 73,
      "question": "Linuxda foydalanuvchi nomini ko‘rish buyrug‘i?",
      "options": ["whoami", "user", "me", "name"],
      "correct": 0
    },
    {
      "id": 74,
      "question": "Qaysi buyrug‘ yordamida katalog ichiga kiriladi?",
      "options": ["cd", "ls", "mkdir", "touch"],
      "correct": 0
    },
    {
      "id": 75,
      "question": "Linuxda faylni nusxalash buyrug‘i?",
      "options": ["cp", "mv", "rm", "ls"],
      "correct": 0
    }
  ],

  "4": [
    {
      "id": 76,
      "question": "Linuxda barcha foydalanuvchilar ro‘yxatini ko‘rish buyrug‘i?",
      "options": ["cat /etc/passwd", "ls -u", "whoami", "userlist"],
      "correct": 0
    },
    {
      "id": 77,
      "question": "Qaysi fayl tizimi Linuxda keng qo‘llaniladi?",
      "options": ["ext4", "FAT16", "NTFS", "exFAT"],
      "correct": 0
    },
    {
      "id": 78,
      "question": "Windows tizimida 'Task Manager'ni qaysi tugmalar bilan chaqiramiz?",
      "options": ["Ctrl + Shift + Esc", "Alt + Tab", "Ctrl + F4", "Ctrl + Alt + Del"],
      "correct": 0
    },
    {
      "id": 79,
      "question": "BIOSga kirish uchun ko‘pincha qaysi tugmalar ishlatiladi?",
      "options": ["F2 yoki Del", "F10 yoki Esc", "Alt + F4", "Ctrl + D"],
      "correct": 0
    },
    {
      "id": 80,
      "question": "Linuxda 'superuser' holatiga o‘tish buyrug‘i?",
      "options": ["sudo su", "cd root", "admin -r", "root"],
      "correct": 0
    },
    {
      "id": 81,
      "question": "Linuxda fonda ishlovchi jarayonlarni ko‘rish buyrug‘i?",
      "options": ["ps", "mv", "top", "kill"],
      "correct": 0
    },
    {
      "id": 82,
      "question": "Windowsda fayl kengaytmasi ko‘rinmasa nima qilish kerak?",
      "options": ["View → File name extensions", "Start → Run", "CMD → .ext", "Edit → Properties"],
      "correct": 0
    },
    {
      "id": 83,
      "question": "Operatsion tizimda 'thread' nima?",
      "options": ["Jarayon ichidagi kichik vazifa", "Tarmoq kabeli", "Kursor", "BIOS menyusi"],
      "correct": 0
    },
    {
      "id": 84,
      "question": "‘Safe mode’ rejimi qachon kerak bo‘ladi?",
      "options": ["Xatoliklarni tuzatishda", "Video tahrirlashda", "Kuchli o‘yinlarda", "Kamera ishlaganda"],
      "correct": 0
    },
    {
      "id": 85,
      "question": "Linuxda log fayllar odatda qayerda saqlanadi?",
      "options": ["/var/log", "/etc/logs", "/log/", "/usr/bin/log"],
      "correct": 0
    },
    {
      "id": 86,
      "question": "Linuxda IP manzilni ko‘rish buyrug‘i?",
      "options": ["ifconfig", "ipconfig", "ipstatus", "netlist"],
      "correct": 0
    },
    {
      "id": 87,
      "question": "Kengaytirilgan xavfsizlik uchun ishlatiladigan OT?",
      "options": ["Qubes OS", "Windows XP", "Android", "ReactOS"],
      "correct": 0
    },
    {
      "id": 88,
      "question": "OS yuklanish tartibi to‘g‘ri ketma-ketlikda?",
      "options": ["BIOS → Bootloader → Kernel → Shell", "Kernel → BIOS → Shell → Bootloader", "Bootloader → BIOS → Kernel", "Shell → BIOS → Bootloader → Kernel"],
      "correct": 0
    },
    {
      "id": 89,
      "question": "Linuxda ishga tushgan dasturlarni o‘ldirish buyrug‘i?",
      "options": ["kill", "rm", "stop", "end"],
      "correct": 0
    },
    {
      "id": 90,
      "question": "OTda fayllarni indekslash maqsadi nima?",
      "options": ["Qidiruvni tezlashtirish", "Faylni yashirish", "Zaxiralash", "Tizimni o‘chirish"],
      "correct": 0
    },
    {
      "id": 91,
      "question": "Windows’da 'System32' papkasi nima?",
      "options": ["Tizim fayllari saqlanadigan joy", "Video fayllar", "Multimedia drayverlari", "Interfeys sozlamalari"],
      "correct": 0
    },
    {
      "id": 92,
      "question": "Linuxda disk hajmini ko‘rish buyrug‘i?",
      "options": ["df -h", "du", "size -d", "fdisk"],
      "correct": 0
    },
    {
      "id": 93,
      "question": "Windowsda faylni qayerdan qayta tiklash mumkin?",
      "options": ["Recycle Bin", "Task Manager", "Settings", "CMD"],
      "correct": 0
    },
    {
      "id": 94,
      "question": "Android qurilmalarida OS yangilanishi qanday amalga oshiriladi?",
      "options": ["OTA orqali", "DVD bilan", "Linux buyruqlari bilan", "BIOS orqali"],
      "correct": 0
    },
    {
      "id": 95,
      "question": "Linuxda barcha jarayonlar ro‘yxatini ko‘rish buyrug‘i?",
      "options": ["ps -aux", "run -all", "jobs", "tasklist"],
      "correct": 0
    },
    {
      "id": 96,
      "question": "Yuklash sektori (boot sector) nima vazifani bajaradi?",
      "options": ["Tizimni ishga tushurish", "Brauzer yuklash", "Kamera sozlash", "Ekran rezolyutsiyasini o‘zgartirish"],
      "correct": 0
    },
    {
      "id": 97,
      "question": "Windowsda diskni formatlash uchun ishlatiladigan vosita?",
      "options": ["Disk Management", "Task Manager", "CMD", "Notepad"],
      "correct": 0
    },
    {
      "id": 98,
      "question": "Qaysi buyruq bilan faylga ruxsat o‘zgartiriladi?",
      "options": ["chmod", "touch", "mv", "ls -a"],
      "correct": 0
    },
    {
      "id": 99,
      "question": "Operatsion tizimning GUI varianti qanday interfeys?",
      "options": ["Grafik interfeys", "Buyruq satri", "Server paneli", "Kameraning interfeysi"],
      "correct": 0
    },
    {
      "id": 100,
      "question": "Linuxda katalogga kirish buyrug‘i?",
      "options": ["cd", "ls", "rm", "mv"],
      "correct": 0
    }
  ],


  "5": [
    {
      "id": 101,
      "question": "Linuxda buyruq satrini tozalash buyrug‘i?",
      "options": ["clear", "reset", "clean", "cls"],
      "correct": 0
    },
    {
      "id": 102,
      "question": "Linuxda .deb fayl qaysi distributivga tegishli?",
      "options": ["Debian", "RedHat", "Arch", "Gentoo"],
      "correct": 0
    },
    {
      "id": 103,
      "question": "OTlarda foydalanuvchini autentifikatsiya qilish nima?",
      "options": ["Shaxsni aniqlash", "IP manzilni olish", "Fayl o‘chirish", "Internet ulash"],
      "correct": 0
    },
    {
      "id": 104,
      "question": "Bootloader'lar misoli qaysi?",
      "options": ["GRUB", "Bash", "BIOS", "UEFI"],
      "correct": 0
    },
    {
      "id": 105,
      "question": "Windows’da kompyuterni qayta yuklash buyrug‘i?",
      "options": ["shutdown /r", "restart", "reload", "boot"],
      "correct": 0
    },
    {
      "id": 106,
      "question": "Linuxda tizimni to‘xtatish buyrug‘i?",
      "options": ["shutdown now", "exit", "logout", "halt"],
      "correct": 0
    },
    {
      "id": 107,
      "question": "Yadroni modifikatsiya qilishda qanday xavf bo‘ladi?",
      "options": ["Tizim ishlamay qolishi", "Internet uzilishi", "Disk to‘lishi", "Printer ishdan chiqishi"],
      "correct": 0
    },
    {
      "id": 108,
      "question": "Virtual xotira nima?",
      "options": ["Haqiqiy bo‘lmagan lekin foydalaniladigan xotira", "Fleshka", "SSD xotira", "BIOS xotira"],
      "correct": 0
    },
    {
      "id": 109,
      "question": "Linuxda jarayon raqamini ko‘rish uchun buyruq?",
      "options": ["ps", "kill", "pid", "proc"],
      "correct": 0
    },
    {
      "id": 110,
      "question": "Windowsda .exe fayl nima bildiradi?",
      "options": ["Bajariluvchi fayl", "Matn fayli", "Rasm fayli", "Zaxira fayl"],
      "correct": 0
    },
    {
      "id": 111,
      "question": "Linuxda buyruqga yordam olish uchun?",
      "options": ["man", "help", "--help", "info"],
      "correct": 0
    },
    {
      "id": 112,
      "question": "Bash bu —",
      "options": ["Buyruq satri muhiti", "Katalog", "Tizim fayli", "Fayl kengaytmasi"],
      "correct": 0
    },
    {
      "id": 113,
      "question": "‘Fork’ bu —",
      "options": ["Jarayon yaratish", "Driver o‘chirish", "Fayl ko‘chirish", "BIOS sozlash"],
      "correct": 0
    },
    {
      "id": 114,
      "question": "Terminal emulyatori nima?",
      "options": ["Buyruq satriga o‘xshash dastur", "Grafik muharrir", "Kompilyator", "Operativ xotira"],
      "correct": 0
    },
    {
      "id": 115,
      "question": "Qaysi tizim GUI'siz ishlaydi?",
      "options": ["FreeDOS", "Windows", "Ubuntu Desktop", "MacOS"],
      "correct": 0
    },
    {
      "id": 116,
      "question": "Linuxda fonda ishlayotgan jarayonni to‘xtatish?",
      "options": ["kill PID", "end task", "pause", "exit"],
      "correct": 0
    },
    {
      "id": 117,
      "question": "Kengaytirilgan foydalanuvchi huquqlari beruvchi buyrug‘?",
      "options": ["sudo", "admin", "root", "power"],
      "correct": 0
    },
    {
      "id": 118,
      "question": "Linuxda fayl nomlarini ajratuvchi belgi?",
      "options": ["/", "\\", ".", ":"],
      "correct": 0
    },
    {
      "id": 119,
      "question": "Qaysi dastur terminalga o‘rnatiladi?",
      "options": ["htop", "word", "photoshop", "chrome"],
      "correct": 0
    },
    {
      "id": 120,
      "question": "Root foydalanuvchining huquqi qanday?",
      "options": ["To‘liq", "Cheklangan", "Faqat o‘qish", "Hech qanday"],
      "correct": 0
    },
    {
      "id": 121,
      "question": "Linuxda .tar.gz bu —",
      "options": ["Arxiv fayli", "Audio fayli", "Matn fayli", "Driver fayli"],
      "correct": 0
    },
    {
      "id": 122,
      "question": "Unix OT oilasiga qaysi kiradi?",
      "options": ["Linux", "Windows", "Android", "MS-DOS"],
      "correct": 0
    },
    {
      "id": 123,
      "question": "OS funksiyasi —",
      "options": ["Resurslarni boshqarish", "Foydalanuvchi ruxsatini cheklash", "Matn tahrirlash", "Sxemalar chizish"],
      "correct": 0
    },
    {
      "id": 124,
      "question": "Linuxda faylni nomini o‘zgartirish?",
      "options": ["mv eski yangi", "cp eski yangi", "rm eski", "rename eski yangi"],
      "correct": 0
    },
    {
      "id": 125,
      "question": "Linuxda yozib bo‘lmaydigan faylga nima denadi?",
      "options": ["read-only", "exec-only", "super-fayl", "input-file"],
      "correct": 0
    }
  ],

  "6": [
    {
      "id": 126,
      "question": "‘Pipe’ bu —",
      "options": ["Ma'lumot uzatish kanali", "USB kabel", "Fayl turi", "Grafik element"],
      "correct": 0
    },
    {
      "id": 127,
      "question": "Qaysi tizim real vaqtda ishlaydi?",
      "options": ["RTOS", "Linux", "Windows", "Android"],
      "correct": 0
    },
    {
      "id": 128,
      "question": "Kernel-mode bu —",
      "options": ["Yadro rejimi", "Oddiy foydalanuvchi rejimi", "Xatolik kodi", "GUI rejimi"],
      "correct": 0
    },
    {
      "id": 129,
      "question": "Foydalanuvchi interfeysi turlari?",
      "options": ["GUI va CLI", "HTML va CSS", "BIOS va CMOS", "CPU va RAM"],
      "correct": 0
    },
    {
      "id": 130,
      "question": "IRQ nima uchun kerak?",
      "options": ["Uskunani keskin ishga tushirish", "Internetga ulanmoq", "Fayl o‘chirish", "BIOS sozlash"],
      "correct": 0
    },
    {
      "id": 131,
      "question": "Qaysi fayl .bashrc fayl hisoblanadi?",
      "options": ["Shell konfiguratsiyasi", "Yadro fayli", "Drayver fayli", "Arxiv fayli"],
      "correct": 0
    },
    {
      "id": 132,
      "question": "Faylga ruxsat beruvchi buyrug‘?",
      "options": ["chmod", "cd", "rm", "ls"],
      "correct": 0
    },
    {
      "id": 133,
      "question": "CLI qisqartmasining ma'nosi?",
      "options": ["Command Line Interface", "Computer Line Instruction", "Central Line Integration", "Command Launch Initiator"],
      "correct": 0
    },
    {
      "id": 134,
      "question": "Windowsda system restore nima qiladi?",
      "options": ["Tizimni qayta tiklaydi", "Fayl o‘chirish", "CD yozish", "Yadro yangilash"],
      "correct": 0
    },
    {
      "id": 135,
      "question": "Linuxda GUI interfeyslaridan biri?",
      "options": ["GNOME", "BIOS", "CMD", "MBR"],
      "correct": 0
    },
    {
      "id": 136,
      "question": "Process va Thread farqi?",
      "options": ["Process mustaqil, Thread ichida ishlaydi", "Thread mustaqil, Process ichida", "Ikkisi bir xil", "Thread bu fayl"],
      "correct": 0
    },
    {
      "id": 137,
      "question": "Shell bu —",
      "options": ["Buyruq satri interfeysi", "Fayl formati", "CD drive", "RAM turi"],
      "correct": 0
    },
    {
      "id": 138,
      "question": "‘Zombie process’ bu —",
      "options": ["Tugatildi, ammo tizimdan chiqarilmagan", "Yangi ishga tushgan", "Xavfli jarayon", "BIOS protsedurasi"],
      "correct": 0
    },
    {
      "id": 139,
      "question": "Caching nima?",
      "options": ["Ma'lumotlarni tezkor saqlash", "Ruxsat berish", "Formatlash", "Zaxiralash"],
      "correct": 0
    },
    {
      "id": 140,
      "question": "OTning eng past darajadagi komponenti?",
      "options": ["Kernel", "GUI", "Shell", "Login manager"],
      "correct": 0
    },
    {
      "id": 141,
      "question": "Faylni arxivlash buyrug‘i (Linux)?",
      "options": ["tar", "ls", "mv", "ps"],
      "correct": 0
    },
    {
      "id": 142,
      "question": "Ishlab chiquvchi uchun eng ochiq tizim?",
      "options": ["Linux", "Windows", "iOS", "macOS"],
      "correct": 0
    },
    {
      "id": 143,
      "question": "Kompyuterda POST testi qachon bajariladi?",
      "options": ["Yoqilganda", "Tizim yuklanganda", "BIOS sozlanganda", "GUI ochilganda"],
      "correct": 0
    },
    {
      "id": 144,
      "question": "Process holati bo‘lishi mumkin?",
      "options": ["Yangi, faol, kutishda", "Fayl, jarayon, direktor", "Uskuna, drayver", "O‘chirilgan, tiklangan"],
      "correct": 0
    },
    {
      "id": 145,
      "question": "Fayl atributi nima?",
      "options": ["Faylga tegishli xossa", "Yadro turi", "Kernel ruxsati", "CPU kodi"],
      "correct": 0
    },
    {
      "id": 146,
      "question": "Linuxda eng yuqori ruxsatga ega foydalanuvchi?",
      "options": ["root", "user", "admin", "guest"],
      "correct": 0
    },
    {
      "id": 147,
      "question": "Xotirani tozalovchi buyrug‘?",
      "options": ["sync", "clear", "wipe", "format"],
      "correct": 0
    },
    {
      "id": 148,
      "question": "System call nima?",
      "options": ["OT funksiyasini chaqirish", "Faylni ochish", "Drayverni o‘rnatish", "IP manzil olish"],
      "correct": 0
    },
    {
      "id": 149,
      "question": "Windowsda msconfig nima?",
      "options": ["Tizim konfiguratsiyasi", "Driver sozlamasi", "BIOS menyusi", "Ekran rezolyutsiyasi"],
      "correct": 0
    },
    {
      "id": 150,
      "question": "MacOS uchun Terminal nima qiladi?",
      "options": ["CLI interfeys taqdim etadi", "iTunes ochadi", "Safari sozlaydi", "Finder o‘chiradi"],
      "correct": 0
    }
  ],


  "7": [
    {
      "id": 151,
      "question": "Tizimdagi vaqtincha fayllar nima uchun kerak?",
      "options": ["Jarayonlar vaqtida ma'lumot saqlash uchun", "Rasmlar saqlash uchun", "Viruslarni yashirish uchun", "BIOS yangilash uchun"],
      "correct": 0
    },
    {
      "id": 152,
      "question": "Linuxda ‘cron’ nima?",
      "options": ["Rejalashtirilgan vazifalar menejeri", "Xavfsizlik tizimi", "BIOS moduli", "Fayl arxivi"],
      "correct": 0
    },
    {
      "id": 153,
      "question": "Tizim resurslari qaysilar?",
      "options": ["Protsessor, xotira, disk", "Telegram, YouTube", "Fleshka, kamera", "Fayllar, papkalar"],
      "correct": 0
    },
    {
      "id": 154,
      "question": "Linuxda `top` buyrug‘i nima qiladi?",
      "options": ["Jarayonlarni ko‘rsatadi", "Fayllarni tozalaydi", "Xotirani to‘ldiradi", "BIOSga kiradi"],
      "correct": 0
    },
    {
      "id": 155,
      "question": "Windows’da `regedit` nima uchun ishlatiladi?",
      "options": ["Reyestrni tahrirlash uchun", "Terminal ochish uchun", "Kamera sozlash", "GUI dizaynini o‘zgartirish"],
      "correct": 0
    },
    {
      "id": 156,
      "question": "Foydalanuvchiga ruxsatlarni beruvchi fayl Linuxda?",
      "options": ["/etc/passwd", "/root/rules", "/var/access", "/usr/lib/user"],
      "correct": 0
    },
    {
      "id": 157,
      "question": "Boot sektor buzilganda nima bo‘ladi?",
      "options": ["OT yuklanmaydi", "Internet ishlamaydi", "Rasm ochilmaydi", "Printer ishlamaydi"],
      "correct": 0
    },
    {
      "id": 158,
      "question": "Windows’da xavfsiz rejimda yuklash uchun nima kerak?",
      "options": ["F8", "Ctrl + Alt + Del", "Shift + F10", "F12"],
      "correct": 0
    },
    {
      "id": 159,
      "question": "Kernel panik holati nima?",
      "options": ["Yadro halokatli xatoga uchradi", "Monitor o‘chadi", "BIOS so‘nadi", "Kamera yoqiladi"],
      "correct": 0
    },
    {
      "id": 160,
      "question": "RedHat qaysi turdagi OT?",
      "options": ["Linux distributivi", "Windows versiyasi", "Mobil OT", "BIOS dasturi"],
      "correct": 0
    },
    {
      "id": 161,
      "question": "Linuxda log yozuvlar uchun qaysi katalog ishlatiladi?",
      "options": ["/var/log", "/etc/log", "/home/logs", "/usr/bin"],
      "correct": 0
    },
    {
      "id": 162,
      "question": "‘Firmware’ bu —",
      "options": ["Qattiq qurilmaga o‘rnatilgan dastur", "Driver fayli", "BIOS interfeysi", "CD fayl"],
      "correct": 0
    },
    {
      "id": 163,
      "question": "Multithreading bu —",
      "options": ["Bir jarayonda bir nechta iplar ishlashi", "Tarmoq kabeli turi", "Virus turi", "Fayl kengaytmasi"],
      "correct": 0
    },
    {
      "id": 164,
      "question": "Linuxda ‘uptime’ buyrug‘i nimani ko‘rsatadi?",
      "options": ["Tizim qancha vaqtdan beri ishlayapti", "Ping vaqtini", "RAM hajmini", "Fayl nomini"],
      "correct": 0
    },
    {
      "id": 165,
      "question": "Windows’dagi ‘blue screen’ sababi?",
      "options": ["Halokatli xatolik", "Ekran yangilanishi", "Kamera yoqilishi", "Signal yetishmasligi"],
      "correct": 0
    },
    {
      "id": 166,
      "question": "Daemon nima?",
      "options": ["Fon jarayon", "GUI oynasi", "Katalog", "Kernel modul"],
      "correct": 0
    },
    {
      "id": 167,
      "question": "Linuxda komanda avvalgi joriy buyrug‘ini ko‘rish?",
      "options": ["history", "previous", "lastcmd", "recent"],
      "correct": 0
    },
    {
      "id": 168,
      "question": "Qanday fayl `.iso` kengaytmaga ega?",
      "options": ["Disk tasviri", "Driver", "Yadro", "BIOS fayli"],
      "correct": 0
    },
    {
      "id": 169,
      "question": "Windows-da ‘cmd’ bu —",
      "options": ["Buyruq oynasi", "Fayl kengaytmasi", "Video dastur", "Driver"],
      "correct": 0
    },
    {
      "id": 170,
      "question": "Linuxda `df` buyrug‘i nimani bildiradi?",
      "options": ["Disk bo‘sh joyini ko‘rsatadi", "Faylni o‘chiradi", "Katalog yaratadi", "Drayverni yuklaydi"],
      "correct": 0
    },
    {
      "id": 171,
      "question": "System call misoli?",
      "options": ["fork()", "sudo", "exit", "print"],
      "correct": 0
    },
    {
      "id": 172,
      "question": "Tizimda konteyner texnologiyasi?",
      "options": ["Docker", "Oracle", "VMware", "WinRAR"],
      "correct": 0
    },
    {
      "id": 173,
      "question": "Kernel modulini qo‘shish buyrug‘i?",
      "options": ["insmod", "chmod", "rm", "exec"],
      "correct": 0
    },
    {
      "id": 174,
      "question": "Linuxda konfiguratsion fayl kengaytmasi odatda?",
      "options": [".conf", ".txt", ".bin", ".sh"],
      "correct": 0
    },
    {
      "id": 175,
      "question": "Jurnal yuritish tizimi nima qiladi?",
      "options": ["Fayl tizimidagi o‘zgarishlarni qayd etadi", "Video yozadi", "BIOSni saqlaydi", "Kernelni zaxiralaydi"],
      "correct": 0
    }
  ],


  "8": [
    {
      "id": 176,
      "question": "Linuxda faylni izlash buyrug‘i?",
      "options": ["find", "search", "scan", "look"],
      "correct": 0
    },
    {
      "id": 177,
      "question": "Virtualizatsiya nima?",
      "options": [
        "Fizik resurslarni dasturiy taqsimlash",
        "Internetdan yuklash",
        "BIOS yangilash",
        "Yadro fayllarini arxivlash"
      ],
      "correct": 0
    },
    {
      "id": 178,
      "question": "Hypervisor bu —",
      "options": [
        "Virtual mashinalarni boshqaruvchi tizim",
        "Windows GUI elementi",
        "Linux distributivi",
        "Shell muhiti"
      ],
      "correct": 0
    },
    {
      "id": 179,
      "question": "Linuxda tarmoq ulanishlarini ko‘rish buyrug‘i?",
      "options": ["netstat", "ifconfig", "ipconfig", "ping"],
      "correct": 0
    },
    {
      "id": 180,
      "question": "CIFS va NFS qaysi maqsadga xizmat qiladi?",
      "options": [
        "Tarmoq fayl almashinuvi",
        "Printer drayverlari",
        "GUI sozlamalari",
        "BIOS interfeysi"
      ],
      "correct": 0
    },
    {
      "id": 181,
      "question": "Linuxda skript fayl kengaytmasi odatda?",
      "options": [".sh", ".exe", ".bat", ".txt"],
      "correct": 0
    },
    {
      "id": 182,
      "question": "Windows-da ‘Task Scheduler’ nima qiladi?",
      "options": [
        "Vazifalarni rejalashtiradi",
        "Sxema chizadi",
        "Faylni ko‘chiradi",
        "BIOSga ulanadi"
      ],
      "correct": 0
    },
    {
      "id": 183,
      "question": "Qaysi OS modulli arxitekturaga ega?",
      "options": ["Linux", "MS-DOS", "FreeDOS", "Android"],
      "correct": 0
    },
    {
      "id": 184,
      "question": "BIOS nima vazifa bajaradi?",
      "options": [
        "Kompyuter ishga tushishini boshlaydi",
        "Rasm tahrirlash",
        "Internet ulash",
        "USB sozlash"
      ],
      "correct": 0
    },
    {
      "id": 185,
      "question": "Linuxda har bir faylning egasi qanday aniqlanadi?",
      "options": ["UID orqali", "IP orqali", "MAC orqali", "PID orqali"],
      "correct": 0
    },
    {
      "id": 186,
      "question": "Yadro kompilyatsiyasi degani —",
      "options": [
        "Yadro kodini moslashtirib yig‘ish",
        "GUI sozlash",
        "BIOSni almashtirish",
        "Kamerani ulang"
      ],
      "correct": 0
    },
    {
      "id": 187,
      "question": "Daemon holatidagi jarayon qayerda ishlaydi?",
      "options": [
        "Fon rejimida",
        "Asosiy interfeysda",
        "Grafik interfeysda",
        "BIOS menyusida"
      ],
      "correct": 0
    },
    {
      "id": 188,
      "question": "Qaysi buyrug‘ bilan skript fayl bajariladi?",
      "options": ["bash script.sh", "run script", "execute script", "open script"],
      "correct": 0
    },
    {
      "id": 189,
      "question": "MBR nima?",
      "options": [
        "Yuklash sektori",
        "Linux distributivi",
        "Drayver turi",
        "Fayl kengaytmasi"
      ],
      "correct": 0
    },
    {
      "id": 190,
      "question": "Windows'ning portativ versiyasi nima deyiladi?",
      "options": [
        "Windows To Go",
        "Windows Fast",
        "WinBoot",
        "Windows Start"
      ],
      "correct": 0
    },
    {
      "id": 191,
      "question": "FAT32 va NTFS o‘rtasidagi asosiy farq?",
      "options": [
        "NTFS xavfsizlik va hajmda afzal",
        "FAT32 grafik interfeysga ega",
        "NTFS bo‘limsiz ishlaydi",
        "FAT32 faqat Linuxda ishlaydi"
      ],
      "correct": 0
    },
    {
      "id": 192,
      "question": "Tizimda zaxira nusxa olish bu —",
      "options": ["Backup", "Restore", "Mirror", "Reboot"],
      "correct": 0
    },
    {
      "id": 193,
      "question": "Linuxda faylni siqish buyrug‘i?",
      "options": ["gzip", "tar -x", "unzip", "du"],
      "correct": 0
    },
    {
      "id": 194,
      "question": "Windows tizim fayllari ko‘p hollarda qayerda joylashgan?",
      "options": ["C:\\Windows\\System32", "D:\\Drivers", "C:\\Program Files", "C:\\My Documents"],
      "correct": 0
    },
    {
      "id": 195,
      "question": "Linux distributivlari farqi nimada?",
      "options": [
        "Paket menejeri, interfeys, yadro sozlamalari",
        "Foydalanuvchi ruxsatida",
        "BIOS menyusida",
        "Kodlash tilida"
      ],
      "correct": 0
    },
    {
      "id": 196,
      "question": "Linuxda root foydalanuvchidan boshqa odatiy foydalanuvchi?",
      "options": ["user", "guest", "admin", "main"],
      "correct": 0
    },
    {
      "id": 197,
      "question": "Windows'da fayl atributlari o‘zgartirish buyrug‘i?",
      "options": ["attrib", "chmod", "perm", "edit"],
      "correct": 0
    },
    {
      "id": 198,
      "question": "Linuxda xizmatlarni boshqarish tizimi?",
      "options": ["systemd", "bootcfg", "lsd", "grub"],
      "correct": 0
    },
    {
      "id": 199,
      "question": "CLI ning afzalligi nima?",
      "options": [
        "Tez ishlaydi, kam resurs sarflaydi",
        "Grafik interfeys chiroyli",
        "Multimedia imkoniyati ko‘p",
        "Faylni ochadi"
      ],
      "correct": 0
    },
    {
      "id": 200,
      "question": "Linuxda 'sudo' bu —",
      "options": [
        "Administrator ruxsatini vaqtincha olish",
        "Drayverni o‘rnatish",
        "Xotirani bo‘shatish",
        "GUI sozlamasi"
      ],
      "correct": 0
    }
  ]








}
# Foydalanuvchi ma'lumotlari
user_data = {}
ratings = {}
ADMIN_IDS = [7871012050]  # Admin ID larini qo'shing

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"),  KeyboardButton(text="2")],
            [KeyboardButton(text="3"), KeyboardButton(text="4")],
            [KeyboardButton(text="5"), KeyboardButton(text="6")], 
            [KeyboardButton(text="7"), KeyboardButton(text="8")], 
            [KeyboardButton(text="👤 Profil"), KeyboardButton(text="📈 Reyting")],  
            [KeyboardButton(text="📞 Adminga murojaat")],
        ],
        resize_keyboard=True
    )
    await message.answer("Quyidagi funksiyalardan birini tanlang:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "⬅️ Ortga")
async def back_to_main_menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
       keyboard=[
            [KeyboardButton(text="1"),  KeyboardButton(text="2")],
            [KeyboardButton(text="3"), KeyboardButton(text="4")],
            [KeyboardButton(text="5"), KeyboardButton(text="6")], 
            [KeyboardButton(text="7"), KeyboardButton(text="8")], 
            [KeyboardButton(text="👤 Profil"), KeyboardButton(text="📈 Reyting")],  
            [KeyboardButton(text="📞 Adminga murojaat")],
        ],
        resize_keyboard=True
    )

    await message.answer("🔙 *Asosiy menyuga qaytdingiz.*", reply_markup=keyboard, parse_mode="Markdown")

@dp.message(lambda message: message.text == "👤 Profil")
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Siz hali test ishlamagansiz! 📌")
        return
    
    user_info = user_data[user_id]
    profile_text = "👤 *Sizning profilingiz:*\n\n"
    for subject, stats in user_info.get("subjects", {}).items():
        profile_text += (
            f"📚 *{subject.capitalize()}*\n"
            f"✅ To'g'ri javoblar: {stats.get('correct', 0)}\n"
            f"❌ Xato javoblar: {stats.get('wrong', 0)}\n"
            f"📊 Jami savollar: {stats.get('total', 0)}\n\n"
        )
    
    profile_text += f"🏆 Umumiy ball: {user_info.get('score', 0)}"
    await message.answer(profile_text, parse_mode="Markdown")

@dp.message(lambda message: message.text == "📈 Reyting")
async def show_ratings(message: types.Message):
    if not ratings:
        await message.answer("📌 Hali hech kim test ishlamagan!")
        return
    
    sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    result = "🏆 *Top 10 Reyting:*\n\n"
    
    for idx, (user_id, score) in enumerate(sorted_ratings[:10], 1):
        try:
            user = await bot.get_chat(user_id)
            name = user.first_name or user.username or f"Foydalanuvchi {user_id}"
            result += f"{idx}. *{name}* - {score} ball\n"
        except Exception as e:
            print(f"Foydalanuvchi ma'lumotlarini olishda xato: {e}")
            result += f"{idx}. Foydalanuvchi {user_id} - {score} ball\n"
    
    await message.answer(result, parse_mode="Markdown")




@dp.message(lambda message: message.text in [
    "1", "2", "3", "4", "5", "6", "7", "8", 

])
async def start_quiz(message: types.Message):
    try:
        user_id = message.from_user.id
        subjects_map = {
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
        }
        
        subject_key = subjects_map.get(message.text)
        if not subject_key:
            await message.answer("❌ Xatolik yuz berdi! Tanlov noto'g'ri.")
            return
        
        
        subject = subjects_map.get(message.text)
        if not subject:
            await message.answer("❌ Xatolik yuz berdi! Tanlov noto'g'ri.")
            return
        
  # Initialize user data if not exists
        if user_id not in user_data:
            user_data[user_id] = {
                "subjects": {},
                "score": 0,
                "current_question": {},
                "all_quizzes": [],
                "current_poll": None,
                "start_time": None
            }
        
        # Get the correct quiz based on subject
        if "tenses" in message.text.lower():
            quiz_type = "tenses"
            if subject_key == "all_tenses":
                tests = []
                for tense in quizzes["tenses"].values():
                    tests.extend(tense)
                random.shuffle(tests)
            else:
                tests = quizzes["tenses"].get(subject_key, [])
        else:
            quiz_type = subject_key
            tests = quizzes.get(quiz_type, [])
        
        if not tests:
            await message.answer("❌ Ushbu test hozircha mavjud emas!")
            return
        
        # Initialize subject data if not exists
        if quiz_type not in user_data[user_id]["subjects"]:
            user_data[user_id]["subjects"][quiz_type] = {
                "correct": 0,
                "wrong": 0,
                "total": 0,
                "current_index": 0,
                "attempts": 0
            }
        
        # Reset quiz progress if starting new quiz
        user_data[user_id]["all_quizzes"] = tests.copy()
        user_data[user_id]["subjects"][quiz_type]["current_index"] = 0
        user_data[user_id]["subjects"][quiz_type]["attempts"] += 1
        user_data[user_id]["start_time"] = time.time()
        
        await message.answer(
            f"📢 {message.text} testi boshlandi!\n\n"
            f"ℹ️ Har bir savolga 30 sekund vaqt beriladi!\n"
            f"🔢 Jami savollar: {len(tests)} ta",
        )
        await send_next_question(user_id, quiz_type, message.text)
        
    except KeyError:
        await message.answer("❌ Ushbu test hozircha mavjud emas!")
    except Exception as e:
        logging.error(f"Error in start_quiz: {e}")
        await message.answer("❌ Testni boshlashda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

async def send_next_question(user_id: int, subject: str, quiz_name: str):
    try:
        # Validate user data
        if user_id not in user_data:
            await bot.send_message(user_id, "❌ Foydalanuvchi ma'lumotlari topilmadi!")
            return
        
        user_info = user_data[user_id]
        questions = user_info.get("all_quizzes", [])
        subject_info = user_info["subjects"][subject]
        quiz_menu = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="⬅️ Testni tugatish")],
            ],
            resize_keyboard=True
        )
        
        await bot.send_message(
            user_id,
            f"🔹 Test: {quiz_name}\n"
            f"🔢 Savol: {subject_info['current_index'] + 1}/{len(questions)}",
            reply_markup=quiz_menu
        )
        # Check if quiz is completed
        if subject_info["current_index"] >= len(questions):
            await show_quiz_results(user_id, subject, quiz_name, subject_info)
            return
        
        question_data = questions[subject_info["current_index"]]
        
        # Validate question data
        if not question_data or "options" not in question_data or "correct" not in question_data:
            await bot.send_message(user_id, "❌ Savol formati noto'g'ri!")
            return
        
        # Prepare options and shuffle
        shuffled_options = question_data["options"].copy()
        correct_answer = shuffled_options[question_data["correct"]]
        random.shuffle(shuffled_options)
        new_correct_index = shuffled_options.index(correct_answer)
        
        # Store current poll data
        user_info["current_poll"] = {
            "poll_id": None,
            "subject": subject,
            "correct_option": new_correct_index,
            "question_index": subject_info["current_index"],
            "quiz_name": quiz_name,
            "start_time": time.time()
        }
        
        # Send the poll question with timer
        poll_msg = await bot.send_poll(
            chat_id=user_id,
            question=question_data["question"],
            options=shuffled_options,
            type="quiz",
            correct_option_id=new_correct_index,
            is_anonymous=False,
            open_period=30  
        )
        
        user_info["current_poll"]["poll_id"] = poll_msg.poll.id
        
    except Exception as e:
        logging.error(f"Error in send_next_question: {e}")
        await bot.send_message(user_id, "❌ Savol yuborishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")


@dp.message(lambda message: message.text == "⬅️ Testni tugatish")
async def finish_quiz_early(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return
    
    if "current_poll" in user_data[user_id]:
        quiz_name = user_data[user_id]["current_poll"]["quiz_name"]
        subject = user_data[user_id]["current_poll"]["subject"]
        await show_quiz_results(user_id, subject, quiz_name, user_data[user_id]["subjects"][subject])



async def show_quiz_results(user_id: int, subject: str, quiz_name: str, subject_info: dict):
    try:



        # Calculate time taken
        time_taken = int(time.time() - user_data[user_id]["start_time"])
        minutes = time_taken // 30
        seconds = time_taken % 30
        


        # Calculate accuracy percentage
        accuracy = 0
        if subject_info['total'] > 0:
            accuracy = (subject_info['correct'] / subject_info['total']) * 100
        

        
        # Prepare result message
        result_text = (
            f"🎉 {quiz_name} testi tugadi!\n\n"
            f"✅ To'g'ri javoblar: {subject_info['correct']}\n"
            f"❌ Noto'g'ri javoblar: {subject_info['wrong']}\n"
            f"📊 Jami savollar: {subject_info['total']}\n"
            f"💯 Aniqlik: {accuracy:.1f}%\n"
            f"⏱ Sarflangan vaqt: {minutes} min {seconds} sec\n\n"
            f"🔢 Urinishlar soni: {subject_info.get('attempts', 1)}"
        )
        
        await bot.send_message(user_id, result_text)
        keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"),  KeyboardButton(text="2")],
            [KeyboardButton(text="3"), KeyboardButton(text="4")],
            [KeyboardButton(text="5"), KeyboardButton(text="6")], 
            [KeyboardButton(text="7"), KeyboardButton(text="8")], 
            [KeyboardButton(text="👤 Profil"), KeyboardButton(text="📈 Reyting")],  
            [KeyboardButton(text="📞 Adminga murojaat")],
        ],
        resize_keyboard=True
    )
    
        await bot.send_message(user_id, "Test muvaffaqiyatli yakunlandi!", reply_markup=keyboard)
        # Update ratings
        ratings[user_id] = user_data[user_id]["score"]
        sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
        user_rank = next((idx for idx, (uid, _) in enumerate(sorted_ratings, 1) if uid == user_id), 0)
        
        await bot.send_message(
            user_id,
            f"🏆 Reytingdagi o'rningiz: {user_rank}\n"
            f"👥 Jami ishtirokchilar: {len(sorted_ratings)}"
        )
        
        # Reset quiz progress
        subject_info.update({
            "total": 0,
            "correct": 0,
            "wrong": 0,
            "current_index": 0
        })
        
    except Exception as e:
        logging.error(f"Error in show_quiz_results: {e}")
        await bot.send_message(user_id, "❌ Natijalarni ko'rsatishda xatolik yuz berdi.")




@dp.poll_answer()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    try:
        user_id = poll_answer.user.id

        # Validate user data
        if user_id not in user_data:
            return

        user_info = user_data[user_id]
        if "current_poll" not in user_info:
            return

        poll_data = user_info["current_poll"]

        # Check if answer is too late (after 35 seconds)
        if time.time() - poll_data.get("start_time", 0) > 35:  # 5 second buffer
            await bot.send_message(user_id, "⏰ Vaqt tugadi! Keyingi savolga o'tamiz.")
            user_info["subjects"][poll_data["subject"]]["wrong"] += 1
            user_info["subjects"][poll_data["subject"]]["total"] += 1
            user_info["subjects"][poll_data["subject"]]["current_index"] += 1
            await send_next_question(user_id, poll_data["subject"], poll_data["quiz_name"])
            return

        # Validate answer
        if not poll_answer.option_ids:
            return  # If user did not select any option, nothing happens

        selected_option = poll_answer.option_ids[0]  # Get selected option
        subject = poll_data["subject"]  # Get current subject
        correct_option = poll_data["correct_option"]  # Get correct answer index
        question_index = poll_data["question_index"]  # Get current question index
        quiz_name = poll_data["quiz_name"]  # Get quiz name

        # Get current question data
        question_data = user_info["all_quizzes"][question_index]
        correct_answer = question_data["options"][question_data["correct"]]  # Correct answer

        # Check if the answer is correct
        if selected_option == correct_option:
            user_info["subjects"][subject]["correct"] += 1  # Increase correct answers count
            user_info["score"] += 1  # Increase overall score
            feedback = "✅ To'g'ri javob!"
        else:
            feedback = f"❌ Noto'g'ri javob! To'g'ri javob: {correct_answer}"  # Show correct answer for wrong choice
            user_info["subjects"][subject]["wrong"] += 1  # Increase wrong answers count

        # Update question stats
        user_info["subjects"][subject]["total"] += 1  # Increase total questions count
        user_info["subjects"][subject]["current_index"] += 1  # Move to next question

        # Send feedback to user
        await bot.send_message(user_id, feedback)

        # Proceed to the next question
        await send_next_question(user_id, subject, quiz_name)

    except Exception as e:
        logging.error(f"Error in handle_poll_answer: {e}")
        if user_id in user_data:
            await bot.send_message(user_id, "❌ Javoblarni qayta ishlashda xatolik yuz berdi.")
    quiz_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Testni tugatish")],
        ],
        resize_keyboard=True
    )
    
    await bot.send_message(
        user_id,
        f"🔹 Test: {poll_data['quiz_name']}\n"
        f"🔢 Keyingi savolga o'tilmoqda...",
        reply_markup=quiz_menu
    )


# Contact admin handler
@dp.message(F.text == "📞 Adminga murojaat")
async def contact_admin(message: Message):
    await message.answer(
        "✍️ Adminga xabar yuborish uchun matn, rasm, video yoki fayl yuboring.\n\n"
        "Yoki to'g'ridan-to'g'ri @admin ga yozishingiz mumkin.",
        reply_markup=types.ReplyKeyboardRemove()
    )

# User to admin message handler
@dp.message(F.chat.type == "private", ~F.from_user.id.in_(ADMIN_IDS))
async def user_to_admin(message: Message):
    try:
        # Format user info
        user_info = (
            f"👤 Foydalanuvchi: {message.from_user.full_name}\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        )
        
        # Forward different message types to admin
        if message.text:
            caption = f"{user_info}📝 Xabar: {message.text}"
            for admin_id in ADMIN_IDS:
                await bot.send_message(admin_id, caption, reply_markup=types.ForceReply())
        
        elif message.photo:
            caption = f"{user_info}📷 Rasm"
            for admin_id in ADMIN_IDS:
                await bot.send_photo(admin_id, message.photo[-1].file_id, 
                                   caption=caption, 
                                   reply_markup=types.ForceReply())
        
        elif message.video:
            caption = f"{user_info}🎥 Video"
            for admin_id in ADMIN_IDS:
                await bot.send_video(admin_id, message.video.file_id, 
                                   caption=caption, 
                                   reply_markup=types.ForceReply())
        
        elif message.document:
            caption = f"{user_info}📄 Fayl: {message.document.file_name}"
            for admin_id in ADMIN_IDS:
                await bot.send_document(admin_id, message.document.file_id, 
                                      caption=caption, 
                                      reply_markup=types.ForceReply())
        
        await message.answer("✅ Xabaringiz adminlarga yuborildi. Javobni kuting.")
    
    except Exception as e:
        logging.error(f"Xabar yuborishda xato: {e}")
        await message.answer("❌ Xabar yuborishda xatolik yuz berdi. Iltimos, keyinroq urunib ko'ring.")

# Admin reply handler
@dp.message(F.reply_to_message, F.from_user.id.in_(ADMIN_IDS))
async def admin_to_user(message: Message):
    try:
        # Extract original message text
        original_msg = message.reply_to_message.text or message.reply_to_message.caption
        
        if original_msg and "👤 Foydalanuvchi:" in original_msg:
            # Extract user ID
            user_id_line = next(line for line in original_msg.split('\n') if "🆔 ID:" in line)
            user_id = int(user_id_line.split(":")[1].strip())
            
            # Send reply to user
            reply_text = (
                "📩 Admin javobi:\n\n"
                f"{message.text}\n\n"
                "💬 Savolingiz bo'lsa, yana yozishingiz mumkin."
            )
            await bot.send_message(user_id, reply_text)
            await message.answer("✅ Javob foydalanuvchiga yuborildi.")
    
    except Exception as e:
        logging.error(f"Javob yuborishda xato: {e}")
        await message.answer("❌ Javob yuborishda xatolik. Foydalanuvchi ID topilmadi.")

# Admin paneli
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Siz admin emassiz!")
        return

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="📢 Reklama yuborish")],
            [KeyboardButton(text="🏠 Asosiy menyu")],  # Asosiy menyuga qaytish tugmasi
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer("👋 Admin panelga xush kelibsiz!", reply_markup=keyboard)

# Asosiy menyuga qaytish
@dp.message(lambda message: message.text == "🏠 Asosiy menyu")
async def back_to_main_menu(message: types.Message):
    await start(message)  # start funksiyasini chaqiramiz

# Admin: Statistika
@dp.message(F.text == "📊 Statistika")
async def show_statistics(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Siz admin emassiz!")
        return

    total_users = len(user_data)  # Foydalanuvchilar sonini hisoblash
    await message.answer(f"📊 Bot foydalanuvchilari soni: {total_users}")

# Admin: Reklama yuborish
# 📢 Admin "Reklama yuborish" tugmasini bossachi
@dp.message(lambda message: message.text == "📢 Reklama yuborish" and message.from_user.id in ADMIN_IDS)
async def ask_for_advertisement(message: Message):
    await message.answer("✍️ Reklama uchun matn, rasm, video yoki fayl yuboring.")

# 📢 Admin xabar, rasm, video yoki fayl yuborsa
@dp.message(lambda message: message.from_user.id in ADMIN_IDS)
async def send_advertisement(message: Message):
    if not user_data:
        await message.answer("⚠️ Hozircha hech qanday foydalanuvchi yo‘q!")
        return

    success, failed = 0, 0

    for user_id in user_data:
        try:
            if message.text:
                await bot.send_message(user_id, message.text)
            elif message.photo:
                await bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                await bot.send_video(user_id, message.video.file_id, caption=message.caption)
            elif message.document:
                await bot.send_document(user_id, message.document.file_id, caption=message.caption)
            success += 1
        except Exception as e:
            print(f"❌ Xabar yuborilmadi (User ID: {user_id}): {e}")
            failed += 1

    await message.answer(f"✅ Reklama {success} ta foydalanuvchiga yuborildi!\n❌ Xatoliklar: {failed}")
# 🎯 Foydalanuvchilarni avtomatik ro‘yxatga olish
@dp.message(lambda message: message.from_user.id not in ADMIN_IDS)
async def register_user(message: Message):
    user_data.add(message.from_user.id)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
