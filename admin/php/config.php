<?php
   use Cloudinary\Configuration\Configuration;
   use Cloudinary\Api\Upload\UploadApi;
    class DatabaseConnection
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
        static function cloudinary_configuration(){
           
        return Configuration::instance([
             'cloud' => [
            'cloud_name' => 'kushvith', 
            'api_key' => '647897594938722', 
            'api_secret' => 'kGd_3nWooLXiIxFW5kSWonWyIZI'],
            'url' => [
           'secure' => true]]);
             }
    }

?>