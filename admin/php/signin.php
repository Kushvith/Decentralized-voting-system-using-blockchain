<?php
include("./jwt.php");
    class Signin{
        private $connection;
        function __construct(PDO $connection){
            $this->connection = $connection;
        }
         function check_user($email,$password){
         
            $query = "select * from staff_login where email = '$email' and password = '$password'";
            $statement = $this->connection->prepare($query);
            $statement->execute();
            $result = $statement->rowCount();
            if($result > 0){
                $type = $this->check_user_type($email);
                if($type['type'] == 0){
                    $token = create_jwt($type['id'],$type['email'],$type['type']);
                    $is_set = set_cookie($token);
                    if($is_set){
                        http_response_code(200);
                        echo json_encode(array("token"=>$token,"role"=>"staff"));
                    }
                }else{
                    echo json_encode(array("message"=>"Admin login"));
                }
            }else{
                http_response_code(400);
                echo json_encode(array("message"=>"You have entered wrong credentials"));
            }
        }
         function check_user_type($email){
            $query = "select * from staff_login where email = '$email'";
            $statement = $this->connection->prepare($query);
            $statement->execute();
            $result = $statement->fetch();
            return $result;
        }
    }
    include("./config.php");
    $connectionObj = new DatabaseConnection();
    $connection = $connectionObj->pdoConnection();
    if(isset($_POST['email'])){
       $signin = new Signin($connection);
       $signin->check_user($_POST['email'],$_POST['password']);
    }

?>