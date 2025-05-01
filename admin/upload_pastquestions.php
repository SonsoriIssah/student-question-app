<?php include("../db.php"); ?>
<!DOCTYPE html>
<html>
<head>
    <title>Upload Past Questions</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 40px;
        }

        .top-right {
            position: absolute;
            top: 20px;
            right: 20px;
        }

        .back-button {
            background-color: #007BFF;
            color: white;
            padding: 10px 16px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }

        .back-button:hover {
            background-color: #0056b3;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h2 {
            text-align: center;
            color: #333;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        select, input[type="file"], input[type="submit"] {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
        }

        input[type="submit"] {
            background-color: #28a745;
            color: white;
            border: none;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #218838;
        }

        .toggle-button {
            background-color: #6c757d;
            color: white;
            padding: 10px 16px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
            margin-top: 15px;
            width: 100%;
        }

        .toggle-button:hover {
            background-color: #5a6268;
        }

        .uploaded-files {
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            display: none;
        }

        .uploaded-files ul {
            list-style-type: none;
            padding: 0;
        }

        .uploaded-files li {
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
        }

        .uploaded-files li:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>

    
    <div class="top-right">
        <a href="dashboard.php" class="back-button">← Back to Dashboard</a>
    </div>

    <div class="container">
        <h2>Upload Past Questions</h2>

        <form action="" method="post" enctype="multipart/form-data">
            <label>Year:</label>
            <select name="year" required>
                <?php for ($y = 2022; $y <= 2030; $y++): ?>
                    <option value="<?= $y ?>"><?= $y ?></option>
                <?php endfor; ?>
            </select>

            <label>Form:</label>
            <select name="form" required>
                <option value="Form 1">Form 1</option>
                <option value="Form 2">Form 2</option>
                <option value="Form 3">Form 3</option>
            </select>

            <label>Course:</label>
            <select name="course" required>
                <option value="General Science">General Science</option>
                <option value="General Arts">General Arts</option>
                <option value="Home Economics">Home Economics</option>
                <option value="Business">Business</option>
                <option value="Visual Arts">Visual Arts</option>
            </select>

            <label>Term:</label>
            <select name="term" required>
                <option value="1st Term">1st Term</option>
                <option value="2nd Term">2nd Term</option>
                <option value="3rd Term">3rd Term</option>
            </select>

            <label>Select PDF Files:</label>
            <input type="file" name="files[]" multiple required>

            <input type="submit" name="upload" value="Upload">
        </form>

        
        <button class="toggle-button" onclick="toggleUploads()">Show Uploaded Files</button>

        <div id="uploadedFilesList" class="uploaded-files">
            <h3>Uploaded Files:</h3>
            <?php
            if (isset($_POST['upload'])) {
                if (isset($_FILES['files']) && count($_FILES['files']['name']) > 0) {
                    $year = $_POST['year'];
                    $form = $_POST['form'];
                    $course = $_POST['course'];
                    $term = $_POST['term'];

                    $target_dir = "../uploads/";
                    if (!file_exists($target_dir)) {
                        mkdir($target_dir, 0777, true);
                    }

                    for ($i = 0; $i < count($_FILES['files']['name']); $i++) {
                        $fileName = $_FILES['files']['name'][$i];
                        $tmpName = $_FILES['files']['tmp_name'][$i];
                        $filePath = $target_dir . basename($fileName);

                        if (move_uploaded_file($tmpName, $filePath)) {
                            $stmt = $conn->prepare("INSERT INTO questions (year, form, course, term, filename, upload_date) VALUES (?, ?, ?, ?, ?, NOW())");
                            $stmt->bind_param("sssss", $year, $form, $course, $term, $fileName);
                            $stmt->execute();
                            echo "<p>Uploaded: $fileName</p>";
                        } else {
                            echo "<p style='color:red;'>Failed: $fileName</p>";
                        }
                    }
                }
            }

           
            $result = $conn->query("SELECT * FROM questions ORDER BY upload_date DESC");
            if ($result->num_rows > 0) {
                echo "<ul>";
                while ($row = $result->fetch_assoc()) {
                    echo "<li>{$row['filename']} — Uploaded: {$row['upload_date']}</li>";
                }
                echo "</ul>";
            } else {
                echo "<p>No files uploaded yet.</p>";
            }
            ?>
        </div>
    </div>

    <script>
        function toggleUploads() {
            const div = document.getElementById("uploadedFilesList");
            div.style.display = div.style.display === "block" ? "none" : "block";
        }
    </script>
</body>
</html>
<?php include("../footer.php"); ?>

