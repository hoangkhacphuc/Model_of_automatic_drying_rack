<?php

require_once 'config.php';

$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

function response($status, $message, $data = null)
{
    $status = $status == 1 ? true : false;
    $response = array(
        'status' => $status,
        'message' => $message,
        'data' => $data
    );
    echo json_encode($response);
}

if (!isset($_GET['action'])) 
    response(0, 'Không tìm thấy action');

$action = $_GET['action'];
session_start();

if (empty($action)) 
    response(0, 'Không tìm thấy action');

switch ($action) {
    case 'login':
        login();
        break;
    case 'logout':
        logout();
        break;
    case 'getHistory':
        getHistory();
        break;
    case 'getSetting':
        getSetting();
        break;
    case 'updateSetting':
        updateSetting();
        break;
    case 'getStatus':
        getStatus();
        break;
    case 'updateAction':
        updateAction();
        break;
    default:
        response(0, 'Không tìm thấy action');
        break;
}

function login()
{
    if (isset($_SESSION['username']))
    {
        response(0, 'Bạn đã đăng nhập rùi mà');
        return;
    }
    global $conn;
    $username = $_POST['username'];
    $password = md5($_POST['password']);

    $sql = "SELECT * FROM `manager` WHERE `username` = '$username' AND `password` = '$password'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $data = array(
            'name' => $row['name'],
        );
        $_SESSION['username'] = $username;
        response(1, 'Đăng nhập thành công rùi nha', $data);
    } else {
        response(0, 'Tài khoản hoặc mật khẩu không chính xác');
    }
}

function getHistory()
{
    global $conn;
    $sql = "SELECT `description`, `created_at`, `status_id` FROM `history` ORDER BY `created_at` DESC";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $data = array();
        while ($row = $result->fetch_assoc()) {
            $data[] = array(
                'description' => $row['description'],
                'created_at' => $row['created_at'],
                'status_id' => $row['status_id']
            );
        }
        response(1, 'Lấy lịch sử thành công', $data);
    } else {
        response(0, 'Không có lịch sử');
    }
}

function getSetting()
{
    global $conn;
    $sql = "SELECT * FROM `setting`";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $data = array();
        while ($row = $result->fetch_assoc()) {
            $data[] = array(
                'id' => $row['id'],
                'name' => $row['name'],
                'data' => $row['data']
            );
        }
        response(1, 'Lấy cài đặt thành công', $data);
    } else {
        response(0, 'Không có cài đặt');
    }
}

function logout()
{
    session_destroy();
    response(1, 'Đăng xuất thành công');
}

function updateSetting()
{
    global $conn;
    $open = $_POST['open'];
    $close = $_POST['close'];

    if (empty($open) || empty($close)) {
        response(0, 'Vui lòng nhập đầy đủ thông tin');
        return;
    }

    if (!isset($_SESSION['username'])) {
        response(0, 'Bạn chưa đăng nhập đâu nha');
        return;
    }

    $open = json_encode(['open' => $open]);
    $close = json_encode(['close' => $close]);

    $sql = "SELECT * FROM `setting` WHERE `data` = '$open' AND `id` = 1";
    $result = $conn->query($sql);
    $open_old = $result->num_rows > 0 ? true : false;

    $sql = "SELECT * FROM `setting` WHERE `data` = '$close' AND `id` = 2";
    $result = $conn->query($sql);
    $close_old = $result->num_rows > 0 ? true : false;

    if ($open_old && $close_old) {
        response(0, 'Không có thay đổi');
        return;
    }

    $sql = "UPDATE `setting` SET `data` = '$open' WHERE `id` = 1";
    $result = $conn->query($sql);

    $sql = "UPDATE `setting` SET `data` = '$close' WHERE `id` = 2";
    $result = $conn->query($sql);

    $description = 'Cập nhật cài đặt';
    $status_id = 7;
    $sql = "INSERT INTO `history` (`description`, `status_id`) VALUES ('$description', '$status_id')";
    $result = $conn->query($sql);

    response(1, 'Cập nhật thành công');
}

function getStatus()
{
    global $conn;
    $sql = "SELECT * FROM `current_status`";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $data = array(
            'open' => $row['open'],
            'sunny' => $row['sunny'],
            'raining' => $row['raining'],
        );
        response(1, 'Lấy trạng thái thành công', $data);
    }
    else {
        response(0, 'Không có trạng thái');
    }
}

function updateAction()
{
    global $conn;
    $action = $_POST['action'];

    if ($action != 0 && $action != 1) {
        response(0, 'Hành động không hợp lệ');
        return;
    }

    if (!isset($_SESSION['username'])) {
        response(0, 'Bạn chưa đăng nhập đâu nha');
        return;
    }

    $sql = "SELECT * FROM `current_status`";
    $result = $conn->query($sql);
    $result = $result->fetch_assoc();
    $open = $result['open'];
    $sunny = $result['sunny'];
    $raining = $result['raining'];
    
    if ($open == $action) {
        response(0, 'Hệ thống hiện đang ở trạng thái này');
        return;
    }

    $sql = "SELECT * FROM `setting`";
    $result = $conn->query($sql);

    $data = array();
    while ($row = $result->fetch_assoc()) {
        $data[] = array(
            'id' => $row['id'],
            'name' => $row['name'],
            'data' => $row['data']
        );
    }

    $time_open = json_decode($data[0]['data'], true)['open'];
    $time_close = json_decode($data[1]['data'], true)['close'];
    $time_open = strtotime($time_open);
    $time_close = strtotime($time_close);
    $time_now = strtotime(date('H:i:s'));

    if ($time_now < $time_open || $time_now > $time_close) {
        response(0, 'Hết giờ làm rùi, tui không nhận tăng ca đâu nha');
        return;
    }

    if ($raining) {
        response(0, 'Ngoài trời vẫn mưa, kéo ra làm chi nữa');
        return;
    }

    if (!$sunny) {
        response(0, 'Trời đã tối rồi, phơi giờ này sương làm ướt đồ đó nha');
        return;
    }

    $sql = "UPDATE `current_status` SET `open` = '$action'";
    $result = $conn->query($sql);

    $description = ($action ? 'Phơi đồ' : 'Thu đồ') . ' thủ công';
    $status_id = ($action ? 4 : 2);
    $sql = "INSERT INTO `history` (`description`, `status_id`) VALUES ('$description', '$status_id')";
    $result = $conn->query($sql);

    response(1, 'Oki nha, giờ tui sẽ ' . ($action ? 'phơi' : 'thu') . ' đồ cho bạn');
}