<!DOCTYPE html>
<html>
<head>
<title>Hackerspace Spacestate</title>
</head>
<body>
This is the update script for the Hackerspace Spaceapi.json.
<pre>
<?php 
print("PHP: Hi NodeMCU. \n");
include("secretsss.php"); 
$_POST = json_decode(file_get_contents('php://input'), true);
//print_r($_POST);
$read_key = substr(trim($_POST['API_key']),0,128);
$sstate = $_POST['sstate'] ;
if ($sstate == 'true') {
    $sstate = 'true';
    print("PHP: SSTATE is True\n");
    } else {
    $sstate = 'false';
    print("PHP: SSTATE is False\n");
    }
 
// Use the temporary Hackerhotel spaceapi.json as example. 
$spaceapi_json = <<<EOT
{
"api": "0.13",
"space": "Hacker Hotel",
"logo": "https://www.tdvenlo.nl/hh/HackerHotel_logo.png",
"url": "https://www.hackerhotel.nl",
"location": {
    "address": "Oud Millingseweg 62, 3886MJ, Garderen, The Netherlands",
    "lat": 52.2208671,
    "lon": 5.7208085
},
"contact": {
    "twitter": "@hotelhacker",
    "email": "info@hackerhotel.nl",
    "facebook": "https://www.facebook.com/hackerhotel/"
},
"issue_report_channels": [
    "email"
],
"state": {
    "open": $sstate,
    "icon": {
        "open": "https://www.tdvenlo.nl/hh/HH_logo_open.png",
        "closed": "https://www.tdvenlo.nl/hh/HH_logo_closed.png"
     },
    "projects": [ "https://hackerhotel.nl/index.php/schedule-2020/" ]
    }
} 
EOT;

if ($read_key != $API_key) {
    die("Wrong key");
}
print("PHP: We got the right key\n");
print("PHP: Space state status: $sstate\n");
$spaceapi_file = fopen('./spaceapi2.json','w') or die ("Unable to open file!");
fwrite($spaceapi_file, $spaceapi_json);
fclose($spaceapi_file);
print("PHP: spaceapi.json written\n");
?>
</pre>
</body>
</html>
