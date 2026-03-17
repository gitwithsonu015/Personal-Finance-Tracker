// Personal Finance Tracker JS Logic
let transactions = JSON.parse(localStorage.getItem('financeTransactions')) || [];
let pieChart = null;
let barChart = null;

const CATEGORIES = ['Food', 'Transport', 'Salary', 'Entertainment', 'Bills', 'Other'];
const COLORS = {
  income: '#10b981',
  expense: '#ef4444',
  pie: ['#f59e0b', '#ef4444', '#10b981', '#8b5cf6', '#06b6d4', '#f97316']
};

// DOM Elements
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const addBtn = document.getElementById('add-btn');
const refreshBtn = document.getElementById('refresh-btn');
const typeSelect = document.getElementById('type');
const categorySelect = document.getElementById('category');
const amountInput = document.getElementById('amount');
const descInput = document.getElementById('description');
const balanceEl = document.getElementById('balance');
const historyBody = document.getElementById('history-body');
const historyRefresh = document.getElementById('history-refresh');



// Init
document.addEventListener('DOMContentLoaded', () => {
  updateTabs();
  renderAll();
  setupEventListeners();
});

function setupEventListeners() {
  // Tab switching
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.dataset.tab;
      switchTab(targetTab);
    });
  });

  // Add transaction
  addBtn.addEventListener('click', addTransaction);

  // Refresh
  refreshBtn.addEventListener('click', renderAll);
  historyRefresh.addEventListener('click', renderHistory);

  // Enter key on inputs
  amountInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTransaction();
  });

}

function switchTab(activeTab) {
  tabBtns.forEach(btn => btn.classList.remove('active'));
  tabContents.forEach(content => content.classList.add('hidden'));
  
  event.target.classList.add('active');
  document.getElementById(activeTab).classList.remove('hidden');
}

function addTransaction() {
  const type = typeSelect.value;
  const category = categorySelect.value;
  const amount = parseFloat(amountInput.value);
  const description = descInput.value.trim();

  if (!amount || amount <= 0 || !category) {
    alert('Please fill amount (>0) and category');
    return;
  }

  const transaction = {
    id: Date.now(),
    date: new Date().toISOString(),
    type,
    category,
    amount,
    description
  };

  transactions.unshift(transaction); // Add to front (newest first)
  saveTransactions();
  
  // Reset form
  amountInput.value = '';
  descInput.value = '';
  
  alert('✅ Transaction added!');
  
  renderAll();
  switchTab('dashboard'); // Switch to dashboard
}

function saveTransactions() {
  localStorage.setItem('financeTransactions', JSON.stringify(transactions));
}

function getBalance() {
  const income = transactions
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0);
  const expense = transactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0);
  return income - expense;
}

function getCategoryTotals() {
  const totals = {};
  transactions
    .filter(t => t.type === 'expense')
    .forEach(t => {
      totals[t.category] = (totals[t.category] || 0) + t.amount;
    });
  return totals;
}

function getMonthlyTrends() {
  const monthly = {};
  transactions.forEach(t => {
    const month = t.date.slice(0, 7); // YYYY-MM
    if (!monthly[month]) monthly[month] = { income: 0, expense: 0 };
    monthly[month][t.type] += t.amount;
  });
  
  return Object.entries(monthly)
    .map(([month, data]) => ({ month, ...data }))
    .sort((a, b) => new Date(b.month) - new Date(a.month))
    .slice(0, 6); // Last 6 months
}

function renderAll() {
  renderBalance();
  renderCharts();
  renderHistory();
}

function renderBalance() {
  const balance = getBalance();
  const formatted = balance.toLocaleString('en-US', { 
    style: 'currency', 
    currency: 'USD',
    minimumFractionDigits: 0 
  });
  balanceEl.textContent = formatted;
  
  // Color based on balance
  balanceEl.parentElement.className = balance >= 0 
    ? 'text-5xl font-black bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent'
    : 'text-5xl font-black bg-gradient-to-r from-red-400 to-rose-500 bg-clip-text text-transparent';
}

function renderCharts() {
  const categoryTotals = getCategoryTotals();
  const monthlyData = getMonthlyTrends();
  
  // Pie Chart
  const pieCtx = document.getElementById('pieChart')?.getContext('2d');
  if (pieCtx && pieChart) pieChart.destroy();
  if (pieCtx && Object.keys(categoryTotals).length) {
    pieChart = new Chart(pieCtx, {
      type: 'pie',
      data: {
        labels: Object.keys(categoryTotals),
        datasets: [{
          data: Object.values(categoryTotals),
          backgroundColor: COLORS.pie.slice(0, Object.keys(categoryTotals).length)
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom', labels: { color: 'white', font: { size: 14 } } } },
        animation: { duration: 1500, easing: 'easeOutBounce' }
      }
    });
  }
  
  // Bar Chart
  const barCtx = document.getElementById('barChart')?.getContext('2d');
  if (barCtx && barChart) barChart.destroy();
  if (barCtx && monthlyData.length) {
    barChart = new Chart(barCtx, {
      type: 'bar',
      data: {
        labels: monthlyData.map(m => m.month),
        datasets: [
          { label: 'Income', data: monthlyData.map(m => m.income), backgroundColor: COLORS.income, borderRadius: 8 },
          { label: 'Expense', data: monthlyData.map(m => m.expense), backgroundColor: COLORS.expense, borderRadius: 8 }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true, ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } },
          x: { ticks: { color: 'white' }, grid: { color: 'rgba(255,255,255,0.1)' } }
        },
        plugins: { legend: { labels: { color: 'white', font: { size: 14 } } } },
        animation: { duration: 1500, easing: 'easeOutQuart' }
      }
    });
  }
}

function renderHistory() {
  historyBody.innerHTML = '';
  if (transactions.length === 0) {
    historyBody.innerHTML = '<tr><td colspan="6" class="p-8 text-center text-xl opacity-75">No transactions yet. Add some! 🎉</td></tr>';
    return;
  }
  
  transactions.slice(0, 50).forEach(t => { // Limit 50
    const row = document.createElement('tr');
    row.className = 'hover:bg-white/20 transition-all border-b border-white/10 transaction-row';
    row.dataset.id = t.id;
    row.innerHTML = `
      <td class="p-4 font-semibold">${new Date(t.date).toLocaleString()}</td>
      <td class="p-4">
        <span class="px-3 py-1 rounded-full text-sm font-bold ${t.type === 'income' ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'}">
          ${t.type.toUpperCase()}
        </span>
      </td>
      <td class="p-4">${t.category}</td>
      <td class="p-4 font-bold text-2xl ${t.type === 'income' ? 'text-green-400' : 'text-red-400'}">
        ${t.type === 'income' ? '+' : '-'}$${t.amount.toFixed(2)}
      </td>
      <td class="p-4 italic">${t.description || '-'}</td>
      <td class="p-4 text-right">
        <button class="delete-btn bg-red-500/80 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105" data-id="${t.id}">🗑️ Delete</button>
      </td>
    `;
    historyBody.appendChild(row);
  });
  
  // Delegate delete events
  historyBody.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', () => deleteTransaction(parseInt(btn.dataset.id)));
  });
}

// Delete transaction function
function deleteTransaction(id) {
  if (confirm('Delete this transaction? This cannot be undone.')) {
    transactions = transactions.filter(t => t.id !== id);
    saveTransactions();
    renderAll();
    alert('🗑️ Transaction deleted!');
  }
}

// Tab switching helper
function updateTabs() {
  const dashboardBtn = document.querySelector('[data-tab="dashboard"]');
  if (dashboardBtn) dashboardBtn.classList.add('active');
  document.getElementById('dashboard').classList.remove('hidden');
}

