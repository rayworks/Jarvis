Vue.component(
    'login-form',
    {
        template: `
        <el-form ref="loginForm" :model="loginForm" :rules="rules" label-width="auto" style="text-align: center">
            <el-form-item prop="username">
                <label for="username" style="padding-right: 5px; margin-bottom: 0px">
                    <i class="el-icon-user"></i>
                </label>
                <el-input v-model="loginForm.username" placeholder="username"></el-input>
            </el-form-item>
            <el-form-item prop="password">
                <label for="password" style="padding-right: 5px; margin-bottom: 0px">
                    <i class="el-icon-lock"></i>
                </label>
                <el-input v-model="loginForm.password" placeholder="password"></el-input>
            </el-form-item>
            <el-form-item>
                <el-checkbox v-model="loginForm.remember" style="line-height: 0.3">Keep Login</el-checkbox>
            </el-form-item>
            <el-form-item>
                <el-button class="sign-in" @click="onSubmit('loginForm')">Sign in</el-button>
            </el-form-item>
        </el-form>`,
        props: {
            login_url: {
                type: String
            }
        },
        data() {
            var validateUsername = (rule, value, callback) => {
                var pattern = /^[A-Za-z][A-Za-z0-9_.]*$/;
                if (pattern.test(value)){
                    callback();
                } else {
                    callback(new Error('Username must have only letters, numbers, dots or underscores'));
                }
            };
            return {
                // registerUrl: this.$props.register_url,
                loginForm: {
                    username: '',
                    password: '',
                    remember: false
                },
                rules: {
                    username: [
                        { min: 1, max: 64, message: 'Length must between 1 and 64.', trigger: 'blur' },
                        { required: true, message: 'Please input username.', trigger: 'blur'},
                        { validator: validateUsername, trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: 'Please input password.', trigger: 'blur'},
                    ]
                }
            }
        },
        methods: {

            onSubmit(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let api = this.$props.login_url;
                        var datas = JSON.stringify({
                            username: this.loginForm.username,
                            password: this.loginForm.password,
                            remember: this.loginForm.remember
                        });
                        let formData = new FormData();
                            for(var key in this.loginForm){
                              formData.append(key,this.loginForm[key]);
                        }
                        console.log(formData);
                        $.ajax({
                            url: api,
                            type: "POST",
                            contentType:"application/json",
                            dataType:"json",
                            data: datas,
                            headers: {"x-csrf-token": csrftoken},
                            processData: false,
                            success: data => {
                                let next_url = data.next_url;
                                location.href = next_url;
                            },
                            error: function (jqXHR, textStatus, errorThrown) {
                                console.log(errorThrown);
                            }
                        });
                    } else {
                        console.log("error submit!!");
                        return false;
                    }
                });
            }

        }
});


Vue.component(
    'register-entry',
    {
        template: `
        <div id="register-container">
            <label for="" style="padding-right: 20px; margin-bottom: 0px">
            </label>
            <p class="register el-input__inner">
                New to JARVIS?
                <a :href="registerUrl" target="_blank">Create an account.</a>
            </p>
        </div>
        `,
        props: {
            register_url: {
                type: String
            }
        },
        data() {
            return {
                registerUrl: this.$props.register_url
            }
        }
});


let vue = new Vue({
    el: '#account-login',
    data: {},
    methods: {},
    created: function () {
    }
});

let registerVue = new Vue({
    el: '#account-register',
    data: {},
    methods: {},
    created: function () {
    }
});
