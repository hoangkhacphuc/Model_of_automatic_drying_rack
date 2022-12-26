$(document).ready(function () {

    $(".close").click(function (e) {
        e.preventDefault();
        const modal = $(this).parents(".modal");
        modal.removeClass("active");
        modal.addClass("hidden");
    });

    $("footer>.item").click(function (e) {
        e.preventDefault();
        const tab = $(this).data("tab");
        $("#" + tab).removeClass("hidden");
        $("#" + tab).addClass("active");

        if (tab == "history") {
            getHistory();
        }
        if (tab == "setting") {
            getSetting();
        }
    });

    $("#btn-login").click(function (e) {
        e.preventDefault();
        const username = $("#username").val();
        const password = $("#password").val();
        $.ajax({
            url: "./API/?action=login",
            type: "POST",
            data: {
                username: username,
                password: password,
            },
            success: function (data) {
                const response = JSON.parse(data);
                if (response.status == false) {
                    swal({
                        icon: './Assets/Images/sorry.jpg',
                        title: 'Thất bại',
                        text: response.message,
                        timer: 2000,
                        showConfirmButton: false
                    });
                } else {
                    swal({
                        icon: './Assets/Images/done.jpg',
                        title: 'Thành công',
                        text: response.message,
                        timer: 2000,
                        showConfirmButton: true
                    }).then(function () {
                        window.location.href = "./";
                    });

                    setTimeout(function () {
                        window.location.href = "./";
                    }, 2000);
                }
            },
            error: function (err) {
                swal({
                    icon: './Assets/Images/error.jpg',
                    title: 'Thất bại',
                    text: 'Đã có lỗi xảy ra, vui lòng thử lại sau!',
                    showConfirmButton: false
                });
            }
        });
    });

    function getHistory() {
        $.ajax({
            url: "./API/?action=getHistory",
            type: "GET",
            success: function (data) {
                const response = JSON.parse(data);
                if (response.status == false) {
                    return;
                }
                const history = response.data;
                var inOut = (param) => {
                    const status = [3, 4, 7, 8];
                    if (status.includes(parseInt(param))) {
                        return "out";
                    }
                    return "in";
                }
                var time = (param) => {
                    return param.split(" ")[1].split(":").slice(0, 2).join(":");
                }
                var date = (param) => {
                    const date = new Date(param);
                    const day = date.getDay();
                    const dayOfMonth = date.getDate();
                    const month = date.getMonth() + 1;
                    const dayOfWeek = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"];
                    return `${dayOfWeek[day]}, ${dayOfMonth} tháng ${month}.`;
                }
                    
                const html = history.map(function (item) {
                    return `
                    <div class="item ${inOut(item.status_id)}">
                        <div class="desc">${item.description}</div>
                        <div class="time">
                            <span>${time(item.created_at)}</span>
                            <span>${date(item.created_at)}</span>
                        </div>
                    </div>`;
                }).join("");
                $("#history-item").html(html);
            },
            error: function (err) {
                swal({
                    icon: './Assets/Images/error.jpg',
                    title: 'Thất bại',
                    text: 'Đã có lỗi xảy ra, vui lòng thử lại sau!',
                    showConfirmButton: false
                });
            }
        });
    }

    function getSetting() {
        $.ajax({
            url: "./API/?action=getSetting",
            type: "GET",
            success: function (data) {
                const response = JSON.parse(data);
                if (response.status == false) {
                    return;
                }
                const time = response.data;
                const open = JSON.parse(time[0].data).open;
                const close = JSON.parse(time[1].data).close;

                $("#time_open").val(open);
                $("#time_close").val(close);
            },
            error: function (err) {
                swal({
                    icon: './Assets/Images/error.jpg',
                    title: 'Thất bại',
                    text: 'Đã có lỗi xảy ra, vui lòng thử lại sau!',
                    showConfirmButton: false
                });
            }
        });
    }

    $('#btn-logout').click(function (e) { 
        e.preventDefault();
        
        $.ajax({
            url: "./API/?action=logout",
            type: "GET",
            success: function (data) {
                const response = JSON.parse(data);
                if (response.status == false) {
                    return;
                }
                swal({
                    icon: './Assets/Images/done.jpg',
                    title: 'Thành công',
                    text: response.message,
                    timer: 2000,
                    showConfirmButton: true
                }).then(function () {
                    window.location.href = "./";
                });

                setTimeout(function () {
                    window.location.href = "./";
                }, 2000);
            },
            error: function (err) {
                swal({
                    icon: './Assets/Images/error.jpg',
                    title: 'Thất bại',
                    text: 'Đã có lỗi xảy ra, vui lòng thử lại sau!',
                    showConfirmButton: false
                });
            }
        });
    });

    $('#btn-update-setting').click(function (e) { 
        e.preventDefault();
        
        const open = $("#time_open").val();
        const close = $("#time_close").val();

        $.ajax({
            url: "./API/?action=updateSetting",
            type: "POST",
            data: {
                open: open,
                close: close
            },
            success: function (data) {
                const response = JSON.parse(data);
                if (response.status == false) {
                    swal({
                        icon: './Assets/Images/sorry.jpg',
                        title: 'Thất bại',
                        text: response.message,
                        timer: 2000,
                        showConfirmButton: false
                    });
                } else {
                    swal({
                        icon: './Assets/Images/done.jpg',
                        title: 'Thành công',
                        text: response.message,
                        timer: 2000,
                        showConfirmButton: false
                    });
                }
            },
            error: function (err) {
                swal({
                    icon: './Assets/Images/error.jpg',
                    title: 'Thất bại',
                    text: 'Đã có lỗi xảy ra, vui lòng thử lại sau!',
                    showConfirmButton: false
                });
            }
        });
    });

    function changeSunny() {
        $('#sun_moon').removeClass('moon');
        $('#sun_moon').addClass('sun');
    }

    function changeMoon() {
        $('#sun_moon').removeClass('sun');
        $('#sun_moon').addClass('moon');
    }

    function changeWet() {
        $('#rain_cloud').addClass('rain');
    }

    function changeDry() {
        $('#rain_cloud').removeClass('rain');
    }

    function changeAction(action) {
        $('.btn_action').addClass(action ? 'on' : 'off');
        $('.btn_action').removeClass(action ? 'off' : 'on');
    }
    changeStatus();

    setInterval(function () {
        changeStatus();
    }, 1000);

    function changeStatus() {
        $.ajax({
            url: "./API/?action=getStatus",
            type: "GET",
            success: function (data) {
                const response = JSON.parse(data);
                if (response.status == false) {
                    return;
                }
                const status = response.data;

                changeAction(parseInt(status.open));
                status.sunny == 1 ? changeSunny() : changeMoon();
                status.raining == 1? changeWet() : changeDry();
            }
        });
    }

    $('.btn_action').click(function (e) { 
        e.preventDefault();
        
        const action = $(this).hasClass('on') ? 0 : 1;
        $.ajax({
            url: "./API/?action=updateAction",
            type: "POST",
            data: {
                action: action
            },
            success: function (data) {
                const response = JSON.parse(data);
                if (response.status == false) {
                    swal({
                        icon: './Assets/Images/sorry.jpg',
                        title: 'Thất bại',
                        text: response.message,
                        timer: 2000,
                        showConfirmButton: false
                    });
                } else {
                    swal({
                        icon: './Assets/Images/done.jpg',
                        title: 'Thành công',
                        text: response.message,
                        timer: 2000,
                        showConfirmButton: false
                    });
                }
            },
            error: function (err) {
                swal({
                    icon: './Assets/Images/error.jpg',
                    title: 'Thất bại',
                    text: 'Đã có lỗi xảy ra, vui lòng thử lại sau!',
                    showConfirmButton: false
                });
            }
        });
    });

    setInterval(function () {
        const time = new Date();
        const hour = time.getHours();
        const minute = time.getMinutes();
        const day = time.getDay();
        const date = time.getDate();
        const month = time.getMonth() + 1;

        const dayOfWeek = ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'];

        $('header>.time').html(`${hour < 10 ? '0' + hour : hour}:${minute < 10 ? '0' + minute : minute}`);
        $('header>.date').html(`${dayOfWeek[day]}, ${date} tháng ${month}`);
    }, 1000);

});
