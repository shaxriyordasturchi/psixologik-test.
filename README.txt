require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');

const app = express();

// Xavfsizlik sozlamalari
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Tezlik cheklovi
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minut
  max: 100 // har IP uchun 100 so'rov
});
app.use(limiter);

// MongoDB ulanish
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/psycho_test_db', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  useCreateIndex: true
})
.then(() => console.log('MongoDB ga ulandi'))
.catch(err => console.error('MongoDB ulanish xatosi:', err));

// Modellar
const User = require('./models/User');
const TestResult = require('./models/TestResult');
const Admin = require('./models/Admin');

// API endpointlari

// Admin kirishi
app.post('/api/admin/login', [
  body('username').trim().notEmpty(),
  body('password').trim().notEmpty()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    const { username, password } = req.body;
    const admin = await Admin.findOne({ username });
    
    if (!admin || !bcrypt.compareSync(password, admin.password)) {
      return res.status(401).json({ message: "Noto'g'ri foydalanuvchi nomi yoki parol" });
    }
    
    const token = jwt.sign({ id: admin._id, username }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.json({ token });
  } catch (error) {
    console.error('Kirish xatosi:', error);
    res.status(500).json({ message: 'Server xatosi' });
  }
});

// Foydalanuvchilar ro'yxati
app.get('/api/admin/users', async (req, res) => {
  try {
    const { page = 1, limit = 10, search = '' } = req.query;
    const skip = (page - 1) * limit;
    
    const query = {};
    if (search) {
      query.$or = [
        { name: { $regex: search, $options: 'i' } },
        { surname: { $regex: search, $options: 'i' } },
        { region: { $regex: search, $options: 'i' } }
      ];
    }
    
    const users = await User.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));
      
    const total = await User.countDocuments(query);
    
    res.json({
      users,
      total,
      pages: Math.ceil(total / limit),
      currentPage: parseInt(page)
    });
  } catch (error) {
    console.error('Foydalanuvchilarni olish xatosi:', error);
    res.status(500).json({ message: 'Server xatosi' });
  }
});

// Test natijalari
app.get('/api/admin/results', async (req, res) => {
  try {
    const { page = 1, limit = 10, region, age } = req.query;
    const skip = (page - 1) * limit;
    
    let query = {};
    if (region) {
      const users = await User.find({ region });
      query.userId = { $in: users.map(u => u._id) };
    }
    
    if (age) {
      const [minAge, maxAge] = age.split('-').map(Number);
      const users = await User.find({ age: { $gte: minAge, $lte: maxAge } });
      query.userId = { $in: users.map(u => u._id) };
    }
    
    const results = await TestResult.find(query)
      .populate('userId')
      .sort({ date: -1 })
      .skip(skip)
      .limit(parseInt(limit));
      
    const total = await TestResult.countDocuments(query);
    
    res.json({
      results,
      total,
      pages: Math.ceil(total / limit),
      currentPage: parseInt(page)
    });
  } catch (error) {
    console.error('Natijalarni olish xatosi:', error);
    res.status(500).json({ message: 'Server xatosi' });
  }
});

// Statistika ma'lumotlari
app.get('/api/admin/stats', async (req, res) => {
  try {
    const totalUsers = await User.countDocuments();
    const totalTests = await TestResult.countDocuments();
    const regions = await User.distinct('region');
    
    res.json({
      totalUsers,
      totalTests,
      totalRegions: regions.length
    });
  } catch (error) {
    console.error('Statistika xatosi:', error);
    res.status(500).json({ message: 'Server xatosi' });
  }
});

// Yangi test natijasini saqlash
app.post('/api/results', [
  body('userData.name').trim().notEmpty(),
  body('userData.surname').trim().notEmpty(),
  body('userData.age').isInt({ min: 7, max: 25 }),
  body('userData.gender').isIn(['Erkak', 'Ayol']),
  body('userData.region').trim().notEmpty(),
  body('results.a').isInt({ min: 0, max: 100 }),
  body('results.b').isInt({ min: 0, max: 100 }),
  body('results.c').isInt({ min: 0, max: 100 })
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    const { userData, results } = req.body;
    
    // Foydalanuvchini saqlash
    const user = new User(userData);
    await user.save();
    
    // Natijalarni saqlash
    const testResult = new TestResult({
      userId: user._id,
      aPercent: results.a,
      bPercent: results.b,
      cPercent: results.c
    });
    await testResult.save();
    
    res.status(201).json({ message: "Natijalar saqlandi", userId: user._id });
  } catch (error) {
    console.error('Natijalarni saqlash xatosi:', error);
    res.status(500).json({ message: 'Server xatosi' });
  }
});

// Server porti
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server ${PORT}-portda ishlayapti`));
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  surname: {
    type: String,
    required: true,
    trim: true
  },
  age: {
    type: Number,
    required: true,
    min: 7,
    max: 25
  },
  gender: {
    type: String,
    required: true,
    enum: ['Erkak', 'Ayol']
  },
  region: {
    type: String,
    required: true,
    trim: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('User', userSchema);
const mongoose = require('mongoose');

const testResultSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  aPercent: {
    type: Number,
    required: true,
    min: 0,
    max: 100
  },
  bPercent: {
    type: Number,
    required: true,
    min: 0,
    max: 100
  },
  cPercent: {
    type: Number,
    required: true,
    min: 0,
    max: 100
  },
  date: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('TestResult', testResultSchema);
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const adminSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  password: {
    type: String,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// Parolni hash qilish
adminSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 10);
  next();
});

module.exports = mongoose.model('Admin', adminSchema);const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const adminSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  password: {
    type: String,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// Parolni hash qilish
adminSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 10);
  next();
});

module.exports = mongoose.model('Admin', adminSchema);
// Asosiy sozlamalar
const API_BASE_URL = 'http://localhost:5000/api';
let currentUser = null;

// DOM elementlari
const elements = {
  // Sahifalar
  pages: {
    welcome: document.getElementById('welcome-page'),
    userInfo: document.getElementById('user-info-page'),
    test: document.getElementById('test-page'),
    results: document.getElementById('results-page'),
    adminLogin: document.getElementById('admin-login-page'),
    adminPanel: document.getElementById('admin-panel')
  },
  
  // Tugmalar
  buttons: {
    startBtn: document.getElementById('start-btn'),
    prevBtn: document.getElementById('prev-btn'),
    nextBtn: document.getElementById('next-btn'),
    submitBtn: document.getElementById('submit-btn'),
    restartBtn: document.getElementById('restart-btn'),
    adminAccessBtn: document.getElementById('admin-access-btn'),
    logoutBtn: document.getElementById('logout-btn'),
    applyFiltersBtn: document.getElementById('apply-filters-btn')
  },
  
  // Formalar
  forms: {
    userForm: document.getElementById('user-form'),
    adminForm: document.getElementById('admin-form')
  },
  
  // Inputlar
  inputs: {
    name: document.getElementById('name'),
    surname: document.getElementById('surname'),
    age: document.getElementById('age'),
    gender: document.getElementById('gender'),
    region: document.getElementById('region'),
    adminUsername: document.getElementById('admin-username'),
    adminPassword: document.getElementById('admin-password'),
    userSearch: document.getElementById('user-search'),
    regionFilter: document.getElementById('region-filter'),
    ageFilter: document.getElementById('age-filter')
  },
  
  // Jadval va diagrammalar
  tables: {
    recentResults: document.querySelector('#recent-results-table tbody'),
    usersTable: document.querySelector('#users-table tbody'),
    resultsTable: document.querySelector('#results-table tbody')
  },
  
  // Natijalar
  results: {
    userName: document.getElementById('result-user-name'),
    userAge: document.getElementById('result-user-age'),
    userGender: document.getElementById('result-user-gender'),
    userRegion: document.getElementById('result-user-region'),
    aPercent: document.getElementById('a-percent'),
    bPercent: document.getElementById('b-percent'),
    cPercent: document.getElementById('c-percent'),
    aBar: document.getElementById('a-bar'),
    bBar: document.getElementById('b-bar'),
    cBar: document.getElementById('c-bar'),
    aDesc: document.getElementById('a-description'),
    bDesc: document.getElementById('b-description'),
    cDesc: document.getElementById('c-description'),
    summary: document.getElementById('result-summary')
  },
  
  // Statistikalar
  stats: {
    totalUsers: document.getElementById('total-users-count'),
    totalTests: document.getElementById('total-tests-count'),
    totalRegions: document.getElementById('total-regions-count')
  }
};

// Test savollari
const testQuestions = [
  // ... (oldingi savollar bazasi)
];

// Dasturni ishga tushirish
function initApp() {
  setupEventListeners();
  checkAdminAuth();
  loadCharts();
}

// Event listenerlarni sozlash
function setupEventListeners() {
  // Boshlash tugmasi
  elements.buttons.startBtn.addEventListener('click', () => {
    showPage('userInfo');
  });
  
  // Foydalanuvchi ma'lumotlari formasi
  elements.forms.userForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await startTest();
  });
  
  // Test navigatsiyasi
  elements.buttons.prevBtn.addEventListener('click', prevQuestion);
  elements.buttons.nextBtn.addEventListener('click', nextQuestion);
  elements.buttons.submitBtn.addEventListener('click', submitTest);
  
  // Qayta boshlash
  elements.buttons.restartBtn.addEventListener('click', () => {
    showPage('welcome');
    elements.buttons.adminAccessBtn.style.display = 'none';
  });
  
  // Admin paneli
  elements.buttons.adminAccessBtn.addEventListener('click', () => {
    showPage('adminLogin');
    elements.buttons.adminAccessBtn.style.display = 'none';
  });
  
  // Admin kirish formasi
  elements.forms.adminForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await adminLogin();
  });
  
  // Admin chiqish
  elements.buttons.logoutBtn.addEventListener('click', adminLogout);
  
  // Filterlarni qo'llash
  elements.buttons.applyFiltersBtn.addEventListener('click', async () => {
    await loadResultsTable();
  });
  
  // Foydalanuvchi qidirish
  elements.inputs.userSearch.addEventListener('input', debounce(async () => {
    await loadUsersTable();
  }, 300));
}

// Sahifalarni ko'rsatish
function showPage(pageName) {
  // Barcha sahifalarni yashirish
  Object.values(elements.pages).forEach(page => {
    page.classList.remove('active');
  });
  
  // Kerakli sahifani ko'rsatish
  elements.pages[pageName].classList.add('active');
}

// Testni boshlash
async function startTest() {
  // Foydalanuvchi ma'lumotlarini saqlash
  currentUser = {
    name: elements.inputs.name.value.trim(),
    surname: elements.inputs.surname.value.trim(),
    age: parseInt(elements.inputs.age.value),
    gender: elements.inputs.gender.value,
    region: elements.inputs.region.value
  };
  
  // Test sahifasiga o'tish
  showPage('test');
  
  // Javoblarni tozalash
  userAnswers = new Array(testQuestions.length).fill(null);
  
  // Savollarni aralashtirish
  shuffleArray(testQuestions);
  
  // Birinchi savolni yuklash
  currentQuestion = 0;
  loadQuestion();
}

// Test natijalarini yuborish
async function submitTest() {
  // Barcha savollarga javob berilganligini tekshirish
  if (userAnswers.some(answer => answer === null)) {
    alert("Iltimos, barcha savollarga javob bering!");
    return;
  }
  
  // Natijalarni hisoblash
  const aCount = userAnswers.filter(answer => answer === 'A').length;
  const bCount = userAnswers.filter(answer => answer === 'B').length;
  const cCount = userAnswers.filter(answer => answer === 'C').length;
  const total = aCount + bCount + cCount;
  
  const aPercent = Math.round((aCount / total) * 100);
  const bPercent = Math.round((bCount / total) * 100);
  const cPercent = Math.round((cCount / total) * 100);
  
  // Natijalarni ko'rsatish
  showResults(aPercent, bPercent, cPercent);
  
  // Serverga yuborish
  await saveResults(aPercent, bPercent, cPercent);
}

// Natijalarni serverga yuborish
async function saveResults(a, b, c) {
  try {
    const response = await fetch(`${API_BASE_URL}/results`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userData: currentUser,
        results: { a, b, c }
      })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'Natijalarni saqlashda xatolik');
    }
    
    console.log('Natijalar saqlandi:', data);
  } catch (error) {
    console.error('Natijalarni saqlash xatosi:', error);
    alert('Natijalarni saqlashda xatolik yuz berdi. Keyinroq urunib ko\'ring.');
  }
}

// Admin autentifikatsiyasini tekshirish
async function checkAdminAuth() {
  const token = localStorage.getItem('adminToken');
  
  if (token) {
    try {
      const response = await fetch(`${API_BASE_URL}/admin/verify`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        showPage('adminPanel');
        await loadAdminData();
      } else {
        localStorage.removeItem('adminToken');
      }
    } catch (error) {
      console.error('Token tekshirishda xatolik:', error);
      localStorage.removeItem('adminToken');
    }
  }
}

// Admin kirishi
async function adminLogin() {
  const username = elements.inputs.adminUsername.value.trim();
  const password = elements.inputs.adminPassword.value;
  
  try {
    const response = await fetch(`${API_BASE_URL}/admin/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      localStorage.setItem('adminToken', data.token);
      showPage('adminPanel');
      await loadAdminData();
    } else {
      throw new Error(data.message || "Noto'g'ri foydalanuvchi nomi yoki parol!");
    }
  } catch (error) {
    console.error('Kirish xatosi:', error);
    alert(error.message || "Kirishda xatolik yuz berdi. Iltimos, qayta urunib ko'ring.");
  }
}

// Admin chiqishi
function adminLogout() {
  localStorage.removeItem('adminToken');
  showPage('welcome');
  elements.buttons.adminAccessBtn.style.display = 'block';
}

// Admin ma'lumotlarini yuklash
async function loadAdminData() {
  try {
    // Umumiy statistikalar
    const statsResponse = await fetch(`${API_BASE_URL}/admin/stats`);
    const stats = await statsResponse.json();
    
    elements.stats.totalUsers.textContent = stats.totalUsers;
    elements.stats.totalTests.textContent = stats.totalTests;
    elements.stats.totalRegions.textContent = stats.totalRegions;
    
    // Oxirgi test natijalari
    const resultsResponse = await fetch(`${API_BASE_URL}/admin/results?limit=5`);
    const { results } = await resultsResponse.json();
    
    elements.tables.recentResults.innerHTML = '';
    results.forEach(result => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${result.userId.name}</td>
        <td>${result.userId.surname}</td>
        <td>${result.userId.age}</td>
        <td>${result.userId.region}</td>
        <td>${result.aPercent}%</td>
        <td>${result.bPercent}%</td>
        <td>${result.cPercent}%</td>
        <td>${new Date(result.date).toLocaleDateString()}</td>
      `;
      elements.tables.recentResults.appendChild(row);
    });
    
    // Foydalanuvchilar jadvali
    await loadUsersTable();
    
    // Natijalar jadvali
    await loadResultsTable();
    
    // Diagrammalar
    await loadCharts();
    
  } catch (error) {
    console.error('Admin ma\'lumotlarini yuklash xatosi:', error);
    alert('Ma\'lumotlarni yuklashda xatolik yuz berdi. Yangilab ko\'ring.');
  }
}

// Foydalanuvchilar jadvalini yuklash
async function loadUsersTable() {
  try {
    const search = elements.inputs.userSearch.value.trim();
    const response = await fetch(`${API_BASE_URL}/admin/users?search=${search}`);
    const { users } = await response.json();
    
    elements.tables.usersTable.innerHTML = '';
    users.forEach(user => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${user._id}</td>
        <td>${user.name}</td>
        <td>${user.surname}</td>
        <td>${user.age}</td>
        <td>${user.gender}</td>
        <td>${user.region}</td>
        <td>1</td>
        <td>${new Date(user.createdAt).toLocaleDateString()}</td>
      `;
      elements.tables.usersTable.appendChild(row);
    });
  } catch (error) {
    console.error('Foydalanuvchilarni yuklash xatosi:', error);
  }
}

// Natijalar jadvalini yuklash
async function loadResultsTable() {
  try {
    const region = elements.inputs.regionFilter.value;
    const age = elements.inputs.ageFilter.value;
    
    let url = `${API_BASE_URL}/admin/results`;
    const params = [];
    
    if (region) params.push(`region=${region}`);
    if (age) params.push(`age=${age}`);
    
    if (params.length > 0) {
      url += `?${params.join('&')}`;
    }
    
    const response = await fetch(url);
    const { results } = await response.json();
    
    elements.tables.resultsTable.innerHTML = '';
    results.forEach(result => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${result._id}</td>
        <td>${result.userId.name} ${result.userId.surname}</td>
        <td>${result.userId.age}</td>
        <td>${result.userId.region}</td>
        <td>${result.aPercent}%</td>
        <td>${result.bPercent}%</td>
        <td>${result.cPercent}%</td>
        <td>${new Date(result.date).toLocaleDateString()}</td>
      `;
      elements.tables.resultsTable.appendChild(row);
    });
  } catch (error) {
    console.error('Natijalarni yuklash xatosi:', error);
  }
}

// Diagrammalarni yuklash
async function loadCharts() {
  try {
    // Hududlar bo'yicha diagramma
    const regionsResponse = await fetch(`${API_BASE_URL}/admin/stats/regions`);
    const regionsData = await regionsResponse.json();
    
    const regionsCtx = document.getElementById('regions-chart').getContext('2d');
    new Chart(regionsCtx, {
      type: 'bar',
      data: {
        labels: regionsData.map(item => item._id),
        datasets: [{
          label: 'Testlar soni',
          data: regionsData.map(item => item.count),
          backgroundColor: '#3498db'
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
    
    // Yosh guruhlari bo'yicha diagramma
    const agesResponse = await fetch(`${API_BASE_URL}/admin/stats/ages`);
    const agesData = await agesResponse.json();
    
    const agesCtx = document.getElementById('ages-chart').getContext('2d');
    new Chart(agesCtx, {
      type: 'pie',
      data: {
        labels: ['7-12 yosh', '13-18 yosh', '19-25 yosh'],
        datasets: [{
          data: [
            agesData['7-12'] || 0,
            agesData['13-18'] || 0,
            agesData['19-25'] || 0
          ],
          backgroundColor: ['#3498db', '#f1c40f', '#2ecc71']
        }]
      },
      options: {
        responsive: true
      }
    });
    
    // Jinslar bo'yicha diagramma
    const gendersResponse = await fetch(`${API_BASE_URL}/admin/stats/genders`);
    const gendersData = await gendersResponse.json();
    
    const gendersCtx = document.getElementById('genders-chart').getContext('2d');
    new Chart(gendersCtx, {
      type: 'doughnut',
      data: {
        labels: ['Erkak', 'Ayol'],
        datasets: [{
          data: [
            gendersData['Erkak'] || 0,
            gendersData['Ayol'] || 0
          ],
          backgroundColor: ['#3498db', '#e74c3c']
        }]
      },
      options: {
        responsive: true
      }
    });
  } catch (error) {
    console.error('Diagrammalarni yuklash xatosi:', error);
  }
}

// Qo'shimcha yordamchi funksiyalar
function debounce(func, wait) {
  let timeout;
  return function() {
    const context = this, args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(context, args);
    }, wait);
  };
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// Dasturni ishga tushirish
document.addEventListener('DOMContentLoaded', initApp);
