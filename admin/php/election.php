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
                $result = $this->mysqlconnection->query("insert into election (name,time_election,status) values ('$name','$time','prnding')");
                if ($result) {
                    return true;
                }
            }
        }
    }
    function check_date_availability($date)
    {
        $result = $this->mysqlconnection->query("select * from election where time_election='$date'");
        if ($result->num_rows > 0) {
            return true;
        }
        return false;
    }
    function get_election_data()
    {
        $table = "";
        $result = $this->mysqlconnection->query("select * from election");
        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                $table .= "<tr>
                    <td>" . $row['name'] . "</td>
                    <td>" . $row['time_election'] . "</td>
                    <td><button class='btn btn-primary btn-sm party-btn' width='20px' data-id=" . $row['id'] . " data-toggle='modal' data-target='#exampleModal'>Add party</button></td>
                    <td>" . $row['status'] . "</td>
                    <td>" . $row['time_creation'] . "</td>
                    <td>action button</td>
                    </tr>
                    ";
            }
        }
        return $table;
    }
}
$connectionObj = new connection();
$connection = $connectionObj->mysqlConnection();
$election = new Election($connection);
if (isset ($_POST['election_name'])) {
    echo $election->create_election($_POST['election_name'], $_POST['time']);
}
if (isset ($_GET['table'])) {
    echo $election->get_election_data();
}
?>