<?php
include ("./jwt.php");
include ("./voter.php");
class contact extends voter
{

    function __construct(PDO $connection){
        parent::__construct($connection);
    }
    function fetch()
    {
        $output = '
        <table class="table">
        <thead>
           <tr>
             <th scope="col" class=" ">Name</th>
            <th scope="col" class=" ">Email</th>
            <th scope="col" class=" ">Message</th>
            <th scope="col" class=" ">Time</th>
            <th scope="col" class=" ">Action</th>
            </tr>
        </thead>
        <tbody>
        ';
        $sql = "SELECT * FROM contact order by id desc";
        $statement = $this->pdoConnection->prepare($sql);
        $statement->execute();
        $result = $statement->fetchAll();
     foreach($result as $row) {
        $output .= '      <tr>
        <td>'.$row['name'].'</td>
        <td>'.$row['email'].'</td>
        <td>'.$row['message'].'</td>
        <td>'.$row['timestamp'].'</td>
        <td>
        <button class="btn btn-success btn-sm contact-reply" data-toggle="modal" data-target="#exampleModal" title="view"  data-id="'.$row['email'].'">Reply</button>    
        <button class="btn btn-danger btn-sm" id="delete"  data-id="'.$row['id'].'">delete</button>    
        </td>
        </tr>
            </tbody>';
     }
     $output .=  '  </table>';
     return $output;

    }
    function create_announcement($val){
        $sql = "INSERT INTO `announcement` (`message`, `time_stamp`) VALUES ('$val', current_timestamp())";
        $statement = $this->pdoConnection->prepare($sql);
        $statement->execute();
        return true;
    }
    function view_announcement(){
        $output = "";
        $sql = "select * from announcement";
        $statement = $this->pdoConnection->prepare($sql);
        $statement->execute();
        $result = $statement->fetchAll();
        foreach($result as $row){
            $output .= '  <div class="col-lg-3 col-md-4">
            <div class="card h-100">
              <div class="card-body">
                <p class="text-primary pt-2">'.$row['message'].'</p>
              </div>
              <div class="card-footer ms-auto">
                <button class="btn btn-danger" id="delete" data-id="'.$row['id'].'">delete</button>
              </div>
            </div>
          </div>';
        }
        return $output;
    }
    function delete($id){
        $sql = "DELETE FROM `announcement` WHERE id = '$id'";
        $statement = $this->pdoConnection->prepare($sql);
        $statement->execute();
        return true;
    }
    function contact_delete($id){
        $sql = "DELETE FROM `contact` WHERE id = '$id'";
        $statement = $this->pdoConnection->prepare($sql);
        $statement->execute();
        return true;
    }
    function contact_reply($email,$message){
        return $this->phpMailer($email,"Reply From Admin",$message);
    }
}

include_once("./config.php");
$connectionObj = new DatabaseConnection();
$connection = $connectionObj->pdoConnection();
$contact = new contact($connection);
if(isset($_GET['table_data'])){
    echo $contact->fetch();
}
if(isset($_POST['announce_text'])){
    echo $contact->create_announcement($_POST['announce_text']);
}
if(isset($_GET['ann_data'])){
    echo $contact->view_announcement();
}
if(isset($_POST['id'])){
    echo $contact->delete($_POST['id']);
}
if(isset($_POST['Contact_id'])){
    echo $contact->contact_delete($_POST['Contact_id']);
}
if(isset($_POST['email'],$_POST['message'])){
    echo $contact->contact_reply($_POST['email'],$_POST['message']);
}
?>