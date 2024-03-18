<?php   
   

   require '../../vendor/autoload.php';
    
   use Firebase\JWT\JWT;
   use Firebase\JWT\Key;
    define("key","1a3LM3W966D6QTJ5BJb9opunkUcw_d09NCOIJb9QZTsrneqOICoMoeYUDcd_NfaQyR787PAH98Vhue5g938jdkiyIZyJICytKlbjNBtebaHljIR6-zf3A2h3uy6pCtUFl1UhXWnV6madujY4_3SyUViRwBUOP-UudUL4wnJnKYUGDKsiZePPzBGrF4_gxJMRwF9lIWyUCHSh-PRGfvT7s1mu4-5ByYlFvGDQraP4ZiG5bC1TAKO_CnPyd1hrpdzBzNW4SfjqGKmz7IvLAHmRD-2AMQHpTU-hN2vwoA-iQxwQhfnqjM0nnwtZ0urE6HjKl6GWQW-KLnhtfw5n_84IRQ");
    function create_jwt($userID,$username,$role){
        $token = JWT::encode(
            array(
                'iat'		=>	time(),
                'nbf'		=>	time(),
                'exp'		=>	time()+2*60*60,
                'data'	=> array(
                    'user_id'	=>	$userID,
                    'user_name'	=>	$username,
                    'role' => $role
                )
            ),
            key,
            'HS256'
        );
        return $token;
    }

    
    function validate_jwt($token){
        try{
        $decoded = JWT::decode($token, new Key(key, 'HS256'));
        return $decoded->data;
        }
        catch(Exception $e){
            return $e->getMessage();
        }
    }

    function set_cookie($token){
        setcookie("token", $token, time() + 3600, "/", "", true, true);
        return true;
    }
    

    // echo create_jwt(1,"kushvith","staff");
    // echo validate_jwt("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MTA3NDkyOTUsIm5iZiI6MTcxMDc0OTI5NSwiZXhwIjoxNzEwNzU2NDk1LCJkYXRhIjp7InVzZXJfaWQiOjEsInVzZXJfbmFtZSI6Imt1c2h2aXRoIiwicm9sZSI6InN0YWZmIn19.VvI6ERlZXuM4_BT4nUvh1vhqbaCSkM0Oz1Y2TMWwX-4");

?>