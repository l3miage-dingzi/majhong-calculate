import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Shanten } from './shanten';

describe('Shanten', () => {
  let component: Shanten;
  let fixture: ComponentFixture<Shanten>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Shanten]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Shanten);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
