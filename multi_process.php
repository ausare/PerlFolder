<?php
#phpinfo();
$weekFolder = $_POST["weekFolder"];
$url = $_REQUEST["backURL"];
$target_dir = "Images/" . $weekFolder . "/";
$target_dir_two = "/Volumes/Scans/Ready For Production/" . $weekFolder . "/";
$movie_archive = "Images/Movies/";
$photolist;
#echo "Here's where it's going " . $target_file . ".";
#$photoCount = count($_FILES["fileToUpload"]["tmp_name"]);
#$maxNum = 49;
#if (($photoCount > $maxNum) or ($photoCount == 0)) { 
#				echo "File count is " . $photoCount . "<br>";
#	    		echo "Maximum file upload reached. Redirecting to previous page in 3 seconds.";
#				sleep(3);
#				header("Location: $url");
#}
#$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
	foreach ($_FILES["fileToUpload"]["tmp_name"] as $index => $tmpName) {
			#$photoCount = count($index($tmpName));
			#$maxNum = 49;
				$weekFolder = substr($_FILES["fileToUpload"]["name"][$index], -7, 3);
				$target_dir = "Images/" . $weekFolder . "/";
				$target_dir_two = "/Volumes/Scans/Ready For Production/" . $weekFolder . "/";
				$target_file = $target_dir . ($_FILES["fileToUpload"]["name"][$index]);
				$target_file_two = $target_dir_two . ($_FILES["fileToUpload"]["name"][$index]);
				if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"][$index], $target_file)) {
    			    #echo "The file ". $fileName . " has been uploaded.";
					copy($target_file,$target_file_two);
					$photolist = $photolist."|".($_FILES["fileToUpload"]["name"][$index]);
					if (strpos(($_FILES["fileToUpload"]["name"][$index]), 'cmov') !== false) {
						copy($target_file,$movie_archive . ($_FILES["fileToUpload"]["name"][$index]));
					}
    			} else {
    			    echo "Sorry, there was an error uploading $target_file.";
    	 		   echo $_POST["weekFolder"];
				}
	}
}
header("Location: $url");
		header('Location: '.$url.'&weekof='.$weekFolder.'&feature='.$photolist);
?>                                                        