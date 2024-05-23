<?php
    include_once ("./config.php");
    use \PHPMailer\PHPMailer\PHPMailer;
    require_once 'phpmailer/Exception.php';
    require_once 'phpmailer/PHPMailer.php';
    require_once 'phpmailer/SMTP.php';
    class voter{
        protected $pdoConnection;
        function __construct(PDO $connection){
            $this->pdoConnection = $connection;
        }

        function fetchUnverifiedVoters(){
            $output = "";
            $sql = "select * from voters where status = 0";
            $statement = $this->pdoConnection->prepare($sql);
            $statement->execute();
            $result = $statement->fetchAll();
            if($result){
                foreach($result as $row){
                    $output .='
                    <tr>
                    <td>'.$row['first_name'] .' '.$row['last_name'] .'</td>
                        <td>'.$row['dob'].'</td>
                        <td>'.$row['email'].'</td>
                        <td>'.$row['phone'].'</td>
                        <td>'.$row['pan'].'</td>
                        <td> <button class="btn btn-sm btn-success" id="verify" data-id="'.$row['id'].'">Verify</button>
                        <button class="btn btn-sm btn-danger" id="delete" data-id="'.$row['id'].'">delete</button>
                        </td>
                        </tr>
                    ';
                }
                return $output;
            }else{
                return "<td col-span='3'>No Pending Voter Verification</td>";
            }
        }
        function fetchEmail($id){
            $sql ="select * from voters where id=$id";
            $statement = $this->pdoConnection->prepare($sql);
            $statement->execute();
            return $statement->fetch(); 
        }
        function verify($id){
            $user = $this->fetchEmail($id);
            if($user){
            $sql = "UPDATE `voters` SET `status`= 1 where id = $id";
            $statement = $this->pdoConnection->prepare($sql);
            $statement->execute();
            $message = "
                <h1 style='text-align:center;color:green'>".$user['first_name']." ".$user['last_name']." is Verified </ht>
                <p>".$user['email']." is now applicable to vote for the candidates and have right to decide the leader as citizen of the country</p> 
            ";
            $this->phpMailer($user['email'],"Voter Request Verified - E-Voting System",$message);
            return 1;
            }
            else{
                return "Some Error Occured";
            }
        }
        function delete($id){
            $user = $this->fetchEmail($id);
            if($user){
                $sql = "DELETE FROM `voters` WHERE id = $id";
                $statement = $this->pdoConnection->prepare($sql);
                $statement->execute();
                $message = "
                <h1 style='text-align:center;color:green'>".$user['first_name']." ".$user['last_name']." is not Verified </ht>
                <p>".$user['email']." is not applicable to vote for the candidates and You Entered the wrong details double check your details and create 
                    new account</p> 
            ";
            $this->phpMailer($user['email'],"Voter Request not Verified - E-Voting System",$message);
            return 1;
            }
        }
        function phpMailer($email,$title,$message){
            $mail = new PHPMailer(true);
            try{
                $mail->isSMTP();
                $mail->Host = 'smtp.gmail.com';
                $mail->SMTPAuth = true;
                $mail->Username = 'vrlitheesh2002@gmail.com'; 
                $mail->Password = 'gfgbzbwhavhflumm';
                $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
                $mail->Port = '587';
            
                $mail->setFrom($email); 
                $mail->addAddress($email); 
            
                $mail->isHTML(true);
                $mail->Subject = $title;
                $mail->Body = $message;
            
                     $mail->send();
                     return  "success";
                   } catch (Exception $e){
                     return $e->getMessage();            
                   }
        }
    }
    $connectionObj = new DatabaseConnection();
    $connection = $connectionObj->pdoConnection();
    $voter = new voter($connection);
    if(isset($_GET['voter_list'])){
        echo $voter->fetchUnverifiedVoters();
    }
    if(isset($_POST['verify'])){
        echo $voter->verify($_POST['verify']);
    }
    if(isset($_POST['delete'])){
        echo $voter->delete($_POST['delete']);
    }
  
?>