<?php
session_start();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 40px;
        }

        .top-right {
            position: absolute;
            top: 20px;
            right: 20px;
        }

        .logout-button {
            background-color: #dc3545;
            color: white;
            padding: 10px 16px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }

        .logout-button:hover {
            background-color: #c82333;
        }

        .dashboard-container {
            max-width: 500px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        h2 {
            margin-bottom: 30px;
            color: #333;
        }

        .btn {
            display: block;
            width: 100%;
            padding: 14px;
            margin: 15px 0;
            font-size: 16px;
            background-color: #007BFF;
            color: white;
            text-decoration: none;
            border: none;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }

        .btn:hover {
            background-color: #0056b3;
        }

        @media (max-width: 600px) {
            .dashboard-container {
                margin: 10px;
            }

            .btn {
                font-size: 14px;
                padding: 12px;
            }
        }
    </style>
</head>
<body>

<div class="top-right">
    <a href="../logout.php" class="logout-button">Logout</a>
</div>

<div class="dashboard-container">
    <h2>Admin Dashboard</h2>
    <a href="upload_pastquestions.php" class="btn">Upload Past Questions</a>
    <a href="manage_users.php" class="btn">Manage Users</a>
    <a href="view_reports.php" class="btn">View Reports</a>
</div>

</body>
</html>
<?php include("../footer.php"); ?>