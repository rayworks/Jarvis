Vue.component(
    'register-form',
    {
        template: `
        <el-form ref="registerForm" :model="registerForm" :rules="rules" label-width="auto" style="text-align: center">
            <el-form-item prop="username">
                <label for="username" style="padding-right: 5px; margin-bottom: 0px">
                    <i class="el-icon-user"></i>
                </label>
                <el-input v-model="registerForm.username" placeholder="username"></el-input>
            </el-form-item>
            <el-form-item prop="password">
                <label for="password" style="padding-right: 5px; margin-bottom: 0px">
                    <i class="el-icon-lock"></i>
                </label>
                <el-input v-model="registerForm.password" placeholder="password"></el-input>
            </el-form-item>
            <el-form-item prop="confirmPassword">
                <label for="confirmPassword" style="padding-right: 5px; margin-bottom: 0px">
                    <i class="el-icon-lock"></i>
                </label>
                <el-input v-model="registerForm.confirmPassword" placeholder="confirm password"></el-input>
            </el-form-item>
            <el-form-item prop="email">
                <label for="email" style="padding-right: 5px; margin-bottom: 0px">
                    <i class="el-icon-message"></i>
                </label>
                <el-input v-model="registerForm.email" placeholder="email"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button class="sign-in" @click="onSubmit('registerForm')">Sign in</el-button>
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

            var checkPassword = (rule, value, callback) => {
                if (value === '') {
                  callback(new Error('Please input password again.'));
                } else if (value !== this.ruleForm.pass) {
                  callback(new Error('Password is not same as above!'));
                } else {
                  callback();
                }
            };

            return {
                // registerUrl: this.$props.register_url,
                registerForm: {
                    username: '',
                    password: '',
                    confirmPassword: '',
                    email: ''
                },
                rules: {
                    username: [
                        { min: 1, max: 64, message: 'Length must between 1 and 64.', trigger: 'blur' },
                        { required: true, message: 'Please input username.', trigger: 'blur'},
                        { validator: validateUsername, trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: 'Please input password.', trigger: 'blur'},
                    ],
                    confirmPassword: [
                        { validator: checkPassword, trigger: 'blur' }
                    ],
                    email: [
                        { required: true, message: 'Please input email.', trigger: 'blur' },
                        { type: 'email', message: 'Please input correct email.', trigger: ['blur', 'change'] }
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
                            username: this.registerForm.username,
                            password: this.registerForm.password,
                            email: this.registerForm.email
                        });
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

let vue = new Vue({
    el: '#register',
    data: {},
    methods: {},
    created: function () {
    }
});
