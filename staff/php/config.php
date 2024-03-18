<?php
    class connection
    {
        function pdoConnection(){
            try{
            $connection = new PDO("mysql:host=localhost;dbname=decentralized","root","");
            return $connection;
            }
           catch(PDOException $e){
            echo "connection failed" . $e->getMessage();
           }
        }
        function mysqlConnection(){
            $connection = mysqli_connect("localhost","root","","decentralized");
            if(!$connection){
                echo "unable to make the connection";
            }
            return $connection;
        }
    }

?>