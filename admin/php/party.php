<?php
include ("./jwt.php");
include ("./config.php"); 
    class party{
        private $mysqlconnection;
        function __construct(mysqli $connection){
            $this->mysqlconnection = $connection;
        }
        function createparty(){

        }
        function image_uploads(){
            
        }

    }

?>