<?php
session_start();
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>OLAGSHS Student Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet"/>
  <style>
    body {
      font-family: 'Inter', sans-serif;
    }
    ::-webkit-scrollbar {
      width: 8px;
    }
    ::-webkit-scrollbar-thumb {
      background-color: #cbd5e1;
      border-radius: 4px;
    }
  </style>
</head>
<body class="bg-slate-200 min-h-screen flex flex-col">

<div class="flex flex-1 overflow-hidden">
  
  <aside class="flex flex-col w-64 min-h-screen bg-[#00294d] text-white select-none">
    <div class="flex items-center gap-2 px-4 py-3 bg-[#ff9f00]">
      <img src="../olag_logo.jpeg" alt="OLAGSHS logo" class="w-8 h-8" />
      <span class="font-extrabold text-white text-lg leading-none">OLAGSHS</span>
    </div>
    <nav class="flex flex-col flex-1 overflow-y-auto">
      <a href="#" class="flex items-center gap-2 px-4 py-3 text-sm bg-[#003366] hover:bg-[#004080]"><i class="fas fa-th-large text-yellow-400"></i>Dashboard</a>
      
      
      <div class="px-4 py-3 font-semibold text-yellow-400 cursor-pointer" onclick="toggleDropdown()">
        <div class="flex items-center justify-between">
          <span class="flex items-center gap-2"><i class="fas fa-user-friends"></i>Modules</span>
          <i class="fas fa-chevron-down text-yellow-400"></i>
        </div>
        <div id="dropdownMenu" class="flex flex-col mt-3 ml-4 space-y-2 font-normal text-slate-300 hidden">
          <a href="exams.php" class="flex items-center gap-2 hover:text-white"><i class="fas fa-chevron-right text-yellow-400"></i>Exams</a>
          <a href="projections.php" class="flex items-center gap-2 hover:text-white"><i class="fas fa-chevron-right text-yellow-400"></i>Projections</a>
          <a href="daily_notes.php" class="flex items-center gap-2 hover:text-white"><i class="fas fa-chevron-right text-yellow-400"></i>Daily Notes</a>
          <a href="fees.php" class="flex items-center gap-2 hover:text-white"><i class="fas fa-chevron-right text-yellow-400"></i>Fees</a>
          <a href="supplies.php" class="flex items-center gap-2 hover:text-white"><i class="fas fa-chevron-right text-yellow-400"></i>Supplies</a>
        </div>
      </div>

      <div class="mt-auto px-4 py-3">
        <form action="../logout.php" method="post">
          <button type="submit" class="w-full text-center bg-red-600 hover:bg-red-700 px-4 py-2 rounded text-white font-bold">
            Logout
          </button>
        </form>
      </div>
    </nav>
  </aside>

  <?php include("../footer.php"); ?>

  
  <main class="flex-1 flex flex-col overflow-y-auto">
    <header class="flex justify-between items-center px-6 py-3 bg-white border-b border-gray-200">
      <div class="text-yellow-500 font-semibold text-xl">Student Dashboard</div>
      <div class="flex items-center gap-3">
        <div class="text-right text-xs">
          <div class="uppercase font-semibold text-black">SONSORI</div>
          <div class="text-gray-500">Student</div>
        </div>
        <img src="../olag_logo.jpeg" alt="Student Profile" class="w-10 h-10 rounded-full object-cover" />
      </div>
    </header>

    <section class="p-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-7xl mx-auto">
      <a href="view_pastquestions.php" class="bg-yellow-400 rounded-md p-6 text-center text-black shadow hover:shadow-md transition">
        <i class="fas fa-book text-2xl mb-2"></i>
        <div class="font-semibold">Past Questions</div>
        <p class="text-sm">Access uploaded past questions</p>
      </a>
      <a href="exams.php" class="bg-blue-600 rounded-md p-6 text-center text-white shadow hover:shadow-md transition">
        <i class="fas fa-eye text-2xl mb-2"></i>
        <div class="font-semibold">Exams</div>
        <p class="text-sm">View exam results</p>
      </a>
      <a href="daily_notes.php" class="bg-sky-500 rounded-md p-6 text-center text-white shadow hover:shadow-md transition">
        <i class="far fa-clock text-2xl mb-2"></i>
        <div class="font-semibold">Daily Notes</div>
        <p class="text-sm">View your notes</p>
      </a>
      <a href="projections.php" class="bg-red-600 rounded-md p-6 text-center text-white shadow hover:shadow-md transition">
        <i class="fas fa-chart-line text-2xl mb-2"></i>
        <div class="font-semibold">Projections</div>
        <p class="text-sm">Track your performance</p>
      </a>
      <a href="fees.php" class="bg-gray-700 rounded-md p-6 text-center text-white shadow hover:shadow-md transition">
        <i class="fas fa-money-bill-wave text-2xl mb-2"></i>
        <div class="font-semibold">Fees</div>
        <p class="text-sm">Check your balance</p>
      </a>
      <a href="supplies.php" class="bg-green-600 rounded-md p-6 text-center text-white shadow hover:shadow-md transition">
        <i class="fas fa-box text-2xl mb-2"></i>
        <div class="font-semibold">Supplies</div>
        <p class="text-sm">Check requisitions</p>
      </a>
    </section>
  </main>
</div>

<script>
  function toggleDropdown() {
    const menu = document.getElementById("dropdownMenu");
    menu.classList.toggle("hidden");
  }
</script>

</body>
</html>
