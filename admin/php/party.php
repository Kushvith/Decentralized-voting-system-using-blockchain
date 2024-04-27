<?php
include ("./jwt.php");
include ("./config.php"); 
use Cloudinary\Api\Upload\UploadApi;
require_once 'vendor/autoload.php'; 

    class party{
        private $cloudinary;
        private $mysqlconnection;
        function __construct(mysqli $connection){
            $this->mysqlconnection = $connection;
            $cloudinaryConfig = DatabaseConnection::cloudinary_configuration();
            $this->cloudinary = new UploadApi($cloudinaryConfig);
        }
        function createparty($candidate,$party,$age,$filename){
            $imgdata = self::image_uploads($filename);
            $result = $this->mysqlconnection->query("INSERT INTO `party` (`name`, `candidate_name`, `age`, `url`, `publicid`) VALUES ( '$party', '$candidate', '$age', '$imgdata[0]', '$imgdata[1]')");
            if ($result) {
                return true;
            }
        }
        function view_party(){
            $table = "";
            $result = $this->mysqlconnection->query("select * from party");
            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    $table .= "<tr class='text-center'>
                        <td>" . $row['name'] . "</td>
                        <td>" . $row['candidate_name'] . "</td>
                        <td>" . $row['age'] . "</td>
                        <td><img src='" . $row['url'] . "' class='img-responsive w-30 h-30'/></td>
                        <td><button class='btn btn-danger btn-sm' id='delete' data-id=".$row['id'].">delete</td>
                        </tr>
                        ";
                }
            }
            return $table;
        }
        function party_candidate($id){
            $result = $this->mysqlconnection->query("SELECT p.* FROM party p LEFT JOIN election_party ep ON p.id = ep.party_id AND ep.election_id = '$id' WHERE ep.party_id IS NULL;");
         

             echo json_encode($result->fetch_all());

        }
        function party_ele_table($id){
            $table = "";
            $result = $this->mysqlconnection->query("select * from election_party INNER JOIN party on party.id = election_party.party_id where election_id='$id'");
            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    $table .= "<tr class='text-center'>
                        <td>" . $row['name'] . "</td>
                        <td>" . $row['candidate_name'] . "</td>
                        <td>" . $row['age'] . "</td>
                        <td><img src='" . $row['url'] . "' class='img-responsive w-30 h-30'/></td>
                        <td><button class='btn btn-danger btn-sm' id='delete_modal' data-ele=".$id." data-id=".$row['id'].">delete</td>
                        </tr>
                        ";
                }
            }
            return $table;
        }
        function delete($id){
            return $this->mysqlconnection->query("delete from party where id='$id'");
        }
        
         function image_uploads($filename){
          
            $data =  $this->cloudinary->upload($filename,array(
                "folder" => "party",
                "transformation"=>array(
                array("width"=>200, "crop"=>"scale")
                )));
              $url = $data["secure_url"];
              $publicid = $data["public_id"];
              if($url ==""){
                http_response_code(400);
                return json_encode(array("message" => "Cloudinary Error"));
              }
              else{
                return array($url,$publicid);
              }
              
        }
        function party_modal_delete($ele_id,$par_id){
            return $this->mysqlconnection->query("delete from election_party where party_id='$par_id' and election_id = '$ele_id'");
        }
        function party_ele_create($ele_id,$par_id){
                for ($i=0; $i < count($par_id); $i++) { 
                    $result = $this->mysqlconnection->query("INSERT INTO `election_party` (`election_id`, `party_id`) VALUES ('$ele_id', '$par_id[$i]')");
                }
                if($result){
                    return true;
                }
            
           
        }
    }
    $connectionObj = new DatabaseConnection();
    $connection = $connectionObj->mysqlConnection();
    $party = new party($connection);
    if(isset($_POST['age'])){
        $age = $_POST['age'];
        $candidate = $_POST['candidate'];
        $party_name = $_POST['party'];
        $filename = $_FILES["fileimg"]["tmp_name"];
        echo $party->createparty($candidate,$party_name,$age,$filename);
        // echo $party->image_uploads($filename);
         
    }
    if (isset ($_GET['table'])) {
        echo $party->view_party();
    }
    if(isset($_POST['id'])){
        echo $party->delete($_POST['id']);
    }
    if(isset($_POST['party_candidate'])){
        echo $party->party_candidate($_POST['par_id']);
    }
    if(isset($_POST['party_ele_table'])){
        echo $party->party_ele_table($_POST['party_ele_table']);
    }
    if(isset($_POST['election_id']) && isset($_POST['party_id'])){
        echo $party->party_modal_delete($_POST['election_id'],$_POST['party_id']);
    }
    if(isset($_POST['ele_id']) && isset($_POST['par_up_id'])){
        echo $party->party_ele_create($_POST['ele_id'],$_POST['par_up_id']);
    }
?>