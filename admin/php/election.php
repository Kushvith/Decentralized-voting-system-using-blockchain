<?php
include ("./jwt.php");
include ("./config.php");
class Election
{
    private $mysqlconnection;
    function __construct(mysqli $connection)
    {
        $this->mysqlconnection = $connection;
    }

    function create_election($name, $time)
    {
        $date_now = date('Y-m-d');
        $date = date('Y-m-d', strtotime($time));
        if ($date < $date_now) {
            http_response_code(400);
            return json_encode(array("message" => "Date should be future"));
        } else {
            if ($this->check_date_availability($time)) {
                http_response_code(400);
                return json_encode(array("message" => "Already election scheduled on this date"));
            } else {
                $result = $this->mysqlconnection->query("insert into election (name,time_election,status) values ('$name','$time','pending')");
                if ($result) {
                    return true;
                }
            }
        }
    }
    function delete_election($id)
    {
        $sql = "delete from election where id=$id";
        return $this->mysqlconnection->query($sql);
    }
    function check_date_availability($date)
    {
        $result = $this->mysqlconnection->query("select * from election where time_election='$date'");
        if ($result->num_rows > 0) {
            return true;
        }
        return false;
    }
    function fetch_results(){
        $output = "";
        $sql = "SELECT election.id,COUNT(*) as total_parties,election.name,election.time_election FROM `results` INNER JOIN election ON results.election = election.id WHERE election.status = 'completed' GROUP BY results.election";
        $result = $this->mysqlconnection->query($sql);
        if($result->num_rows > 0){
            while ($row = $result->fetch_assoc()) {
                $output .="
                    <tr>
                        <td>".$row['name']."</td>
                        <td>".$row['time_election']."</td>
                        <td>".$row['total_parties']."</td>
                        <td><button class='btn btn-success' data-toggle='modal' data-target='#exampleModal1' id='view' data-id=".$row['id'].">view results</button></td>
                    </tr>
                ";
            }
        }
        return $output;
    }   
    function res_anlalysis($id){
        $output = "";
        $sql = "SELECT party_name, result FROM `results` INNER JOIN election ON results.election = election.id WHERE results.election = $id AND election.status = 'completed' ORDER BY result DESC";
        $result = $this->mysqlconnection->query($sql);
        if($result->num_rows > 0){
            while ($row = $result->fetch_assoc()) {
                $output .="
                    <tr>
                        <td>".$row['party_name']."</td>
                        <td>".$row['result']."</td>
                    </tr>
                ";
            }
        }
        return $output;
    }

    function get_election_data()
    {
        $table = "";
        $result = $this->mysqlconnection->query("select * from election where status = 'pending'");
        if ($result->num_rows > 0) {
            $currentDate = date('Y-m-d');
            $btn = "";
            $partybtn = "";
            while ($row = $result->fetch_assoc()) {
               if($row['time_election'] == $currentDate){
                $btn = "<button class='btn btn-success me-2' id='complete'>Complete</button><button class='btn btn-danger' id='delete' data-id='".$row['id']."'>delete</button>"; 
            }
               else{
                $btn = "<button class='btn btn-danger' id='delete' data-id='".$row['id']."'>delete</button>";
                $partybtn = "<button class='btn btn-primary btn-sm party-btn ' width='20px' data-id=" . $row['id'] . " data-toggle='modal' data-target='#exampleModal'>Add party</button>";
               }
                $table .= "<tr>
                    <td>" . $row['name'] . "</td>
                    <td>" . $row['time_election'] . "</td>
                    <td>$partybtn</td>
                    <td>" . $row['status'] . "</td>
                    <td>" . $row['time_creation'] . "</td>
                    <td>$btn</td>
                    </tr>
                    ";
            }
        }
        return $table;
    }
}
$connectionObj = new DatabaseConnection();
$connection = $connectionObj->mysqlConnection();
$election = new Election($connection);
if (isset ($_POST['election_name'])) {
    echo $election->create_election($_POST['election_name'], $_POST['time']);
}
if (isset ($_GET['table'])) {
    echo $election->get_election_data();
}
if (isset($_POST['delete_id'])){
    echo $election->delete_election($_POST['delete_id']);
}
if(isset($_GET['fetch_res'])){
    echo $election->fetch_results();
}
if(isset($_POST['res_anl'])){
    echo $election->res_anlalysis($_POST['res_anl']);
}
?>