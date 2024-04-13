<?php
include ("./jwt.php");
class contact
{
    private $connection;
    function __construct(PDO $connection){
        $this->connection = $connection;
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
        $statement = $this->connection->prepare($sql);
        $statement->execute();
        $result = $statement->fetchAll();
     foreach($result as $row) {
        $output .= '      <tr>
        <td>'.$row['name'].'</td>
        <td>'.$row['email'].'</td>
        <td>'.$row['message'].'</td>
        <td>'.$row['time'].'</td>
        <td>
        <button class="btn btn-success btn-sm contact-reply" data-bs-toggle="modal" data-bs-target="#exampleModal" title="view"  data-id="'.$row['email'].'">Reply</button>    
        </td>
        </tr>
            </tbody>';
     }
     $output .=  '  </table>';
     return $output;

    }
    function create_announcement($val){
        $sql = "INSERT INTO `announcement` (`message`, `time_stamp`) VALUES ('$val', current_timestamp())";
        $statement = $this->connection->prepare($sql);
        $statement->execute();
        return true;
    }
    function view_announcement(){
        $output = "";
        $sql = "select * from announcement";
        $statement = $this->connection->prepare($sql);
        $statement->execute();
        $result = $statement->fetchAll();
        foreach($result as $row){
            $output .= '  <div class="col-lg-3 col-md-4">
            <div class="card">
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
        $statement = $this->connection->prepare($sql);
        $statement->execute();
        return true;
    }
}

include("./config.php");
$connectionObj = new connection();
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
?>