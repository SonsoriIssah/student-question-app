<?php
session_start();
include("db.php");

$username = "";
$password = "";
$remember = false;


if (isset($_COOKIE['remember_username']) && isset($_COOKIE['remember_password'])) {
    $username = $_COOKIE['remember_username'];
    $password = $_COOKIE['remember_password'];
    $remember = true;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $remember = isset($_POST['remember']);

    $query = "SELECT * FROM users WHERE username = ? AND password = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("ss", $username, $password); 
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        $_SESSION['username'] = $user['username'];
        $_SESSION['role'] = $user['role'];

        if ($remember) {
            setcookie("remember_username", $username, time() + (86400 * 30), "/");
            setcookie("remember_password", $password, time() + (86400 * 30), "/");
        } else {
            setcookie("remember_username", "", time() - 3600, "/");
            setcookie("remember_password", "", time() - 3600, "/");
        }

        if ($user['role'] == 'admin') {
            header("Location: admin/dashboard.php");
        } else {
            header("Location: student/dashboard.php");
        }
        exit;
    } else {
        $error = "Invalid username or password.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>LOGIN PAGE</title>
  <script src="js/tailwind.js"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet"/>
</head>
<body>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-700 to-blue-600 relative">
    <img alt="Background" class="absolute inset-0 w-full h-full object-cover opacity-20 pointer-events-none" src="bg.jpg"/>
    <div class="relative bg-white rounded-md shadow-lg w-full max-w-sm p-8">
      <div class="flex flex-col items-center mb-6">
        <img alt="OLAG logo" class="mb-2" height="64" width="64" src="http://localhost/olagshs_website/olag_logo.jpeg"/>
        <p class="text-center text-base font-semibold">LOGIN PAGE</p>
      </div>

      <?php if (isset($error)): ?>
        <div class="text-red-600 text-sm mb-4 text-center"><?= $error ?></div>
      <?php endif; ?>

      <form class="space-y-5" method="POST">
        <div>
          <label class="block text-xs text-gray-600 mb-1" for="username">Username</label>
          <div class="relative">
            <input class="w-full pr-10 py-2 pl-3 text-sm text-gray-900 bg-blue-50 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                   id="username" type="text" name="username" value="<?= htmlspecialchars($username) ?>" required>
            <i class="fas fa-user absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
          </div>
        </div>

        <div>
          <label class="block text-xs text-gray-600 mb-1" for="password">Password</label>
          <div class="relative">
            <input class="w-full pr-10 py-2 pl-3 text-sm text-gray-900 bg-blue-50 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                   id="password" type="password" name="password" value="<?= htmlspecialchars($password) ?>" required>
            <i class="fas fa-lock absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-gray-600">
          <label class="flex items-center space-x-2">
            <input class="w-3.5 h-3.5 border border-gray-300 rounded" type="checkbox" name="remember" <?= $remember ? 'checked' : '' ?>>
            <span>Remember Me</span>
          </label>
          <a class="text-red-600 hover:underline" href="#">Forgot Password?</a>
        </div>
        <?php include("footer.php"); ?>

        <button class="w-full bg-gradient-to-b from-blue-900 to-blue-700 text-white font-semibold py-3 rounded" type="submit">Login</button>
      </form>
    </div>
  </div>
</body>
</html>
