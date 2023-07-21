import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModifyUserInfoModalComponent } from './modify-user-info-modal.component';

describe('ModifyUserInfoModalComponent', () => {
  let component: ModifyUserInfoModalComponent;
  let fixture: ComponentFixture<ModifyUserInfoModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ModifyUserInfoModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ModifyUserInfoModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
