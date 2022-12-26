<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Giàn phơi quần áo tự động</title>

    <link rel="shortcut icon" href="./Assets/Images/favicon.png" type="image/x-icon">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Nunito&display=swap" rel="stylesheet">

    <script src="https://unpkg.com/ionicons@latest/dist/ionicons.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>

    <link rel="stylesheet" href="./Assets/Css/style.css">
    <script src="./Assets/Js/main.js"></script>
</head>

<?php
    include './API/config.php';
    session_start();
    if (isset($_SESSION['username'])) {
        $username = $_SESSION['username'];

        $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $sql = "SELECT * FROM `manager` WHERE `username` = '$username'";
        $result = $conn->query($sql);
        $row = $result->fetch_assoc();
        $name = $row['name'];
    }
?>

<body>
    <div class="container">
        <header>
            <div class="time">12:00</div>
            <div class="date">T2, 26 tháng 12</div>
        </header>
        <div class="weather">
            <div class="left sun" id="sun_moon">
                <div class="shadow"></div>
                <img src="./Assets/Images/sun.png" alt="" id="sun">
                <img src="./Assets/Images/moon.jpg" alt="" id="moon">
            </div>
            <div class="right rain" id="rain_cloud">
                <img src="./Assets/Images/cloud.png" alt="">
                <img src="./Assets/Images/cloud.png" alt="">
                <img src="./Assets/Images/cloud.png" alt="">
                <div class="raining">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                    <img src="./Assets/Images/raining.png" alt="">
                </div>
            </div>
        </div>
        <div class="action">
            <button class="btn_action on"><span id="on">ON</span><span id="off">OFF</span></button>
        </div>
        <footer>
            <div class="item" data-tab="login">
                <i class="fa fa-user"></i>
                <span>Tài khoản</span>
            </div>
            <div class="item" data-tab="history">
                <i class="fa fa-history"></i>
                <span>Lịch sử</span>
            </div>
            <div class="item" data-tab="setting">
                <i class="fa fa-gear"></i>
                <span>Cài đặt</span>
            </div>
            <div class="item" data-tab="info">
                <i class="fa fa-info"></i>
                <span>Liên hệ</span>
            </div>
        </footer>
        <div class="modal " id="login">
            <div class="modal-header">
                <?php if (!isset($_SESSION['username'])): ?>
                    <div class="not_logined">Bạn chưa đăng nhập</div>
                <?php else: ?>
                    <div class="logined">Xin chào <span><?= $name ?? ''; ?></span></div>
                <?php endif; ?>
                <div class="close" id="close-modal"><i class="fa fa-close"></i></div>
            </div>
            <div class="modal-body">
            <?php if (!isset($_SESSION['username'])): ?>
                <div class="form-input">
                    <input type="text" placeholder="Tên đăng nhập" id="username">
                </div>
                <div class="form-input">
                    <input type="password" placeholder="Mật khẩu" id="password">
                </div>
                <button id="btn-login">Đăng nhập</button>
                <?php else: ?>
                    <button id="btn-logout">Đăng xuất</button>
                <?php endif; ?>
            </div>
        </div>
        <div class="modal" id="history">
            <div class="modal-header">
                <div>Lịch sử hoạt động</div>
                <div class="close" id="close-modal"><i class="fa fa-close"></i></div>
            </div>
            <div class="modal-body">
                <div class="history" id="history-item">
                    <!-- <div class="item in">
                        <div class="desc">Thu quần áo do trời mưa</div>
                        <div class="time">
                            <span>12:00</span>
                            <span>T2, 26 tháng 12</span>
                        </div>
                    </div> -->
                </div>
            </div>
        </div>
        <div class="modal " id="setting">
            <div class="modal-header">
                <div>Cài đặt</div>
                <div class="close" id="close-modal"><i class="fa fa-close"></i></div>
            </div>
            <div class="modal-body">
                <div class="form-input">
                    <label for="time_open">Giờ phơi đồ</label>
                    <input type="time" id="time_open">
                </div>
                <div class="form-input">
                    <label for="time_close">Giờ thu đồ</label>
                    <input type="time" id="time_close">
                </div>
                <button id="btn-update-setting">Lưu</button>
            </div>
        </div>
        <div class="modal " id="info">
            <div class="modal-header">
                <div>Liên hệ</div>
                <div class="close" id="close-modal"><i class="fa fa-close"></i></div>
            </div>
            <div class="modal-body">
                <div class="information">
                    <div class="item">
                        <div class="name">Hoàng Khắc Phúc</div>
                        <div class="code">19010066</div>
                    </div>
                    <div class="item">
                        <div class="name">Đường Ngọc Hà</div>
                        <div class="code">19010056</div>
                    </div>
                    <div class="item">
                        <div class="name">Nguyễn Đức Duy</div>
                        <div class="code">19010054</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>