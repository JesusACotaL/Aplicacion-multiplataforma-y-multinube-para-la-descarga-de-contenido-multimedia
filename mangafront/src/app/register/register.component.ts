import { Component, OnInit } from '@angular/core';
import { FormGroup,FormControl, ValidatorFn, AbstractControl, ValidationErrors } from '@angular/forms';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  formReg: FormGroup;

  constructor(
    private userService: UserService,
    private router: Router
  ) { 
    this.formReg = new FormGroup({
      username: new FormControl(),
      email: new FormControl(),
      password: new FormControl(),
      confirmPassword: new FormControl()
    }, 
      this.checkPasswords
    )
  }

  ngOnInit(): void {
  }

  onSubmit(){
    this.userService.register(this.formReg.value)
    .then(response => {
      this.router.navigate(["/home"]);
    })
    .catch(error =>console.log(error));
  }

  checkPasswords: ValidatorFn = (group: AbstractControl):  ValidationErrors | null => { 
    let pass = group.get('password')!.value;
    let confirmPass = group.get('confirmPassword')!.value
    return pass === confirmPass ? null : { notSame: true }
  }
}

