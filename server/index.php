<?php

require_once ("common.php");

pstart ();

$body .= "<div>\n";
$body .= mklink ("api", "api.php");
$body .= " | ";
$body .= mklink ("readlog", "readlog.php");
$body .= "</div>\n";

$body .= "<form action='api.php'>\n";
$body .= "<input type='text' name='cmd' />\n";
$body .= "<input type='submit' value='Send' />\n";
$body .= "</form>\n";

pfinish ();

?>
