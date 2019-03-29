var mouse = {}, pre_mouse = {};

    var camera, scene, renderer;
    var controls;

    var xu = '1', k = 0, interval;
    var objects = [];
    var targets = {table: [], sphere: [], helix: [], grid: []};

    init();
    animate();
    get_structure(xu, "H", "rgba(53,54,119,.8)");

    function get_structure(xu, symbol = "H", color) {
        var xu_list = xu.split(","), r = 12, border = 2, len = xu_list.length, circle_list = [], dot_list = [],
            html = "", speed_list = [0.01, 0.001, 0.001, 0.001, 0.0005, 0.0005, 0.0005];

        for (var i = 1; i <= len; i++) {
            var w = 140 + 40 * i, x = xu_list[i - 1];
            var circle = "circle_" + i;
            circle_list.push({circle: circle, speed: speed_list[i - 1]});
            html = "<div class=\"circle\" id=\"" + circle + "\" style=\"width:" + w + "px;height:" + w + "px;border-color:" + color + "\">" + html;
            for (var j = 0; j < x; j++) {
                let dot = "dot_" + i + "_" + j;
                let angel = 6.28 / x * j;
                dot_list.push({dot: dot, width: w, angel: angel, speed: speed_list[i - 1]});
                html += "<div class=\"dot\" id=\"" + dot + "\" style=\"background-color:" + color + "\"></div>";
            }
            html += "</div>";
        }
        html += "<div class=\"symbol\" style=\"background-color:" + color + "\">" + symbol + "</div>";
        $(".atom").empty().append(html);
        for (var q = 0; q < dot_list.length; q++) {
            var all = dot_list[q];
            $("#" + all.dot).css('left', Math.sin(k * all.speed + all.angel) * (all.width / 2) + all.width / 2 - r / 2 - border).css('top', Math.cos(k * all.speed + all.angel) * (all.width / 2) + all.width / 2 - r / 2 - border);
        }
        if (interval) clearInterval(interval);

        interval = setInterval(function () {
            for (var q = 0; q < circle_list.length; q++) {
                var all = circle_list[q], speed = k * all.speed * 180 % 360, angel = speed.toFixed(1);
                $("#" + all.circle).css('transform', "rotate(" + angel + "deg)");
            }
            k++;
        }, 10);

    }

    function init() {

        camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 1, 10000);
        camera.position.z = 3000;
        var dragging = false;
        scene = new THREE.Scene();
        //标题
        var title = document.createElement('h1');
        title.className = 'title';
        title.innerText = "1 - 氢 (Hydrogen)";
        var object = new THREE.CSS3DObject(title);
        object.position.x = -650;
        object.position.y = 800;
        object.position.z = 0;
        scene.add(object);
        var etype = document.createElement('h2');
        etype.className = 'etype';
        etype.innerText = "非金属";
        object = new THREE.CSS3DObject(etype);
        object.position.x = -650;
        object.position.y = 730;
        object.position.z = 0;
        scene.add(object);
        var show_list = document.createElement('div');
        show_list.className = 'show_list';
        show_list.innerHTML = "<div class=\"title\">相对原子质量</div><div class=\"content amass\">1.008</div>";
        object = new THREE.CSS3DObject(show_list);
        object.position.x = -850;
        object.position.y = 550;
        object.position.z = 0;
        scene.add(object);
        var show_list = document.createElement('div');
        show_list.className = 'show_list';
        show_list.innerHTML = "<div class=\"title\">电子排布</div><div class=\"content configuration\">1s<sup>1</sup></div>";
        object = new THREE.CSS3DObject(show_list);
        object.position.x = -300;
        object.position.y = 550;
        object.position.z = 0;
        scene.add(object);
        var atom = document.createElement('div');
        atom.className = 'atom';
        object = new THREE.CSS3DObject(atom);
        object.position.x = 200;
        object.position.y = 650;
        object.position.z = 0;
        scene.add(object);

        // table

        for (var i = 0; i < table.length; i += 10) {

            let symbol = table[i];
            let number = table[i + 1];
            let atomic_mass = table[i + 2];
            let element_type = table[i + 3];
            let outer_electron = table[i + 4];
            let electron_configuration = table[i + 5];
            let cn_name = table[i + 6];
            let en_name = table[i + 7];
            let bc1, bc2, bc3, category_name;
            switch (element_type) {
                case 1:
                    bc1 = "rgba(53,54,119,.8)";
                    bc2 = "rgba(46,48,108,.5)";
                    bc3 = "rgba(91,113,150,.8)";
                    category_name = "非金属";
                    break;
                case 2:
                    bc1 = "rgba(21,84,100,.8)";
                    bc2 = "rgba(34,74,106,.5)";
                    bc3 = "rgba(70,134,160,.8)";
                    category_name = "类金属";
                    break;
                case 3:
                    bc1 = "rgba(77,74,150,.8)";
                    bc2 = "rgba(102,100,161,.5)";
                    bc3 = "rgba(122,120,202,.8)";
                    category_name = "卤素";
                    break;
                case 4:
                    bc1 = "rgba(87,49,126,.8)";
                    bc2 = "rgba(96,60,130,.5)";
                    bc3 = "rgba(136,92,177,.8)";
                    category_name = "惰性气体";
                    break;
                case 5:
                    bc1 = "rgba(114,47,61,.8)";
                    bc2 = "rgba(100,50,60,.5)";
                    bc3 = "rgba(192,63,95,.8)";
                    category_name = "碱金属";
                    break;
                case 6:
                    bc1 = "rgba(95,70,55,.8)";
                    bc2 = "rgba(93,73,61,.5)";
                    bc3 = "rgba(151,103,73,.8)";
                    category_name = "碱土金属";
                    break;
                case 7:
                    bc1 = "rgba(58,70,90,.8)";
                    bc2 = "rgba(59,73,98,.5)";
                    bc3 = "rgba(91,113,150,.8)";
                    category_name = "过渡金属";
                    break;
                case 8:
                    bc1 = "rgba(28,100,73,.8)";
                    bc2 = "rgba(34,94,79,.5)";
                    bc3 = "rgba(70,153,132,.8)";
                    category_name = "主族金属";
                    break;
                case 9:
                    bc1 = "rgba(74,57,110,.8)";
                    bc2 = "rgba(80,67,111,.5)";
                    bc3 = "rgba(136,109,199,.8)";
                    category_name = "镧系金属";
                    break;
                case 10:
                    bc1 = "rgba(64,37,80,.8)";
                    bc2 = "rgba(62,41,73,.5)";
                    bc3 = "rgba(138,81,168,.8)";
                    category_name = "锕系金属";
                    break;
                default:
                    bc1 = "rgba(87,49,126,.8)";
                    bc2 = "rgba(96,60,130,.5)";
                    bc3 = "rgba(91,113,150,.8)";
                    category_name = "非金属";
            }

            var element = document.createElement('div');
            element.className = 'element';
            element.style.backgroundColor = bc1;
            if (/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) {
                element.addEventListener('touchend', function () {

                    if (dragging) {

                        return;

                    }
                    $("h1.title").text(number + " - " + cn_name + "（" + en_name + "）");
                    $("h2.etype").text(category_name).css("color", bc3);
                    $(".amass").text(atomic_mass);
                    $(".configuration").html(electron_configuration);
                    get_structure(outer_electron, symbol, bc3);
                }, false);
                element.addEventListener('touchstart', function () {

                    dragging = false;

                }, false);
                element.addEventListener('touchmove', function () {

                    dragging = true;

                }, false);
            } else {
                element.addEventListener('click', function () {
                }, false);
                element.addEventListener('mouseover', function () {
                    this.style.backgroundColor = bc2;
                    $("h1.title").text(number + " - " + cn_name + " (" + en_name + ")");
                    $("h2.etype").text(category_name).css("color", bc3);
                    $(".amass").text(atomic_mass);
                    $(".configuration").html(electron_configuration);
                    get_structure(outer_electron, symbol, bc3);
                }, false);
                element.addEventListener('mouseout', function () {
                    this.style.backgroundColor = bc1;
                }, false);
            }


            var sym = document.createElement('div');
            sym.className = 'symbol';
            sym.textContent = symbol;
            var num = document.createElement('div');
            num.className = 'number';
            num.textContent = number;
            sym.appendChild(num);
            var en = document.createElement('div');
            en.className = 'en_name';
            en.textContent = en_name;
            sym.appendChild(en);
            element.appendChild(sym);

            var object = new THREE.CSS3DObject(element);
            object.position.x = Math.random() * 4000 - 2000;
            object.position.y = Math.random() * 4000 - 2000;
            object.position.z = Math.random() * 4000 - 2000;
            scene.add(object);

            objects.push(object);

            var object = new THREE.Object3D();
            object.position.x = (table[i + 8] * 180 - 1730);
            object.position.y = -(table[i + 9] * 180) + 990;

            targets.table.push(object);

        }

        renderer = new THREE.CSS3DRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('container').appendChild(renderer.domElement);


        controls = new THREE.TrackballControls(camera, renderer.domElement);
        controls.rotateSpeed = 1;
        controls.minDistance = 500;
        controls.maxDistance = 6000;
        //是否不平移
        controls.noPan = true;
        controls.noRotate = true;
        controls.addEventListener('change', render);


        function scaleCamera() {

            camera.fov = 5000;
            camera.updateProjectionMatrix();
            renderer.render(scene, camera);

        }


        transform(targets.table, 2000);

        window.addEventListener('resize', onWindowResize, false);
        // document.addEventListener( 'mouseup', onDocumentMouseUp, false );
        document.onmousedown = onDocumentMouseUp;
        document.addEventListener('touthmove', onDocumentTouchMove, false);

    }

    function transform(targets, duration) {

        TWEEN.removeAll();

        for (var i = 0; i < objects.length; i++) {

            var object = objects[i];
            var target = targets[i];

            new TWEEN.Tween(object.position)
                .to({
                    x: target.position.x,
                    y: target.position.y,
                    z: target.position.z
                }, Math.random() * duration + duration)
                .easing(TWEEN.Easing.Exponential.InOut)
                .start();

            new TWEEN.Tween(object.rotation)
                .to({
                    x: target.rotation.x,
                    y: target.rotation.y,
                    z: target.rotation.z
                }, Math.random() * duration + duration)
                .easing(TWEEN.Easing.Exponential.InOut)
                .start();

        }

        new TWEEN.Tween(this)
            .to({}, duration * 2)
            .onUpdate(render)
            .start();

    }

    function onWindowResize() {

        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();

        renderer.setSize(window.innerWidth, window.innerHeight);

        render();

    }

    function onDocumentMouseUp(event) {

        event.preventDefault();
        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
        console.info(mouse);
        //适配手机
        if (event.touches) {

            mouse.x = (event.touches[0].pageX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.touches[0].pageY / window.innerHeight) * 2 + 1;
            pre_mouse.x = mouse.x;
            pre_mouse.y = mouse.y;

        }

    }

    function onDocumentTouchMove() {

        is_move = true;
        mouse.x = (event.touches[0].pageX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.touches[0].pageY / window.innerHeight) * 2 + 1;
        pre_mouse.x = mouse.x;
        pre_mouse.y = mouse.y;

    }

    function animate() {

        requestAnimationFrame(animate);

        TWEEN.update();

        controls.update();

    }

    function render() {

        renderer.render(scene, camera);

    }
