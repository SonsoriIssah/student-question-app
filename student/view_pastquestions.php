<?php include("../db.php"); ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>View Past Questions</title>
  
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
<body>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>View Past Questions</h2>
      <a href="dashboard.php" class="btn btn-danger">BACK</a>
    </div>

    <form method="get" action="" class="mb-4">
      <div class="row g-3">
        <div class="col-md-3">
          <label for="year" class="form-label">Year</label>
          <select class="form-select" name="year" id="year">
            <option value="">All</option>
            <?php
              for ($y = 2022; $y <= 2030; $y++) {
                $selected = (isset($_GET['year']) && $_GET['year'] == $y) ? 'selected' : '';
                echo "<option value='$y' $selected>$y</option>";
              }
            ?>
          </select>
        </div>

        <div class="col-md-3">
          <label for="form" class="form-label">Form</label>
          <select class="form-select" name="form" id="form">
            <option value="">All</option>
            <?php
              $forms = ["Form 1", "Form 2", "Form 3"];
              foreach ($forms as $f) {
                $selected = (isset($_GET['form']) && $_GET['form'] == $f) ? 'selected' : '';
                echo "<option value='$f' $selected>$f</option>";
              }
            ?>
          </select>
        </div>

        <div class="col-md-3">
          <label for="course" class="form-label">Course</label>
          <select class="form-select" name="course" id="course">
            <option value="">All</option>
            <?php
              $courses = ["General Science", "General Arts", "Home Economics", "Business", "Visual Arts"];
              foreach ($courses as $c) {
                $selected = (isset($_GET['course']) && $_GET['course'] == $c) ? 'selected' : '';
                echo "<option value='$c' $selected>$c</option>";
              }
            ?>
          </select>
        </div>

        <div class="col-md-3">
          <label for="term" class="form-label">Term</label>
          <select class="form-select" name="term" id="term">
            <option value="">All</option>
            <?php
              $terms = ["1st Term", "2nd Term", "3rd Term"];
              foreach ($terms as $t) {
                $selected = (isset($_GET['term']) && $_GET['term'] == $t) ? 'selected' : '';
                echo "<option value='$t' $selected>$t</option>";
              }
            ?>
          </select>
        </div>
      </div>
      <button type="submit" class="btn btn-primary mt-3">Filter</button>
    </form>
   
    <?php
      $query = "SELECT * FROM questions WHERE 1=1";

      if (!empty($_GET['year'])) {
        $year = $_GET['year'];
        $query .= " AND year='$year'";
      }
      if (!empty($_GET['form'])) {
        $form = $_GET['form'];
        $query .= " AND form='$form'";
      }
      if (!empty($_GET['course'])) {
        $course = $_GET['course'];
        $query .= " AND course='$course'";
      }
      if (!empty($_GET['term'])) {
        $term = $_GET['term'];
        $query .= " AND term='$term'";
      }

      $result = $conn->query($query);

      echo "<ul class='list-group'>";
      if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
          echo "<li class='list-group-item'>
                  <strong>{$row['year']} - {$row['form']} - {$row['course']} - {$row['term']}</strong>
                  <br><a href='../uploads/{$row['filename']}' target='_blank'>Download</a>
                </li>";
        }
      } else {
        echo "<li class='list-group-item text-danger'>No past questions found for the selected filters.</li>";
      }
      echo "</ul>";
    ?>
  </div>

  
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
<?php include("../footer.php"); ?>
