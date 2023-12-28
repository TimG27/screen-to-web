<?php

$filename = $_FILES['file']['name'];
$location = "upload/".$filename;

move_uploaded_file ($_FILES['file']['tmp_name'], $location);

?>