import { Component, Input, OnInit, Output } from '@angular/core';
import {FormControl} from '@angular/forms';
import {Observable} from 'rxjs';
import {map, startWith} from 'rxjs/operators';
import { Roles } from '../champ-input-area/champ-input-area.component';
import { JsonFetcherService } from '../json-fetcher.service';

@Component({
  selector: 'app-champ-input-field',
  templateUrl: './champ-input-field.component.html',
  styleUrls: ['./champ-input-field.component.scss']
})
export class ChampInputFieldComponent implements OnInit {

  constructor(private jsonFetcher: JsonFetcherService){
  }

  @Input() role: string = ''
  data: {} | null = null
  name_list: string[] = []
  init: boolean = false;
  myControl = new FormControl();
  options: string[] = [];
  filteredOptions: Observable<string[]>;
  name_val: string = '';
  showLabel: boolean = true;

  updateNameVal = (e:any ) =>{
    this.name_val = e.target.value;

  }

  getDropdownImage(name: string, width = 20){
    return this.jsonFetcher.getImageSource(name, width)
  }

  getWholeRoleName(role: string){
    if(role === 'top'){
      return role;
    } else if(role === 'bot'){
      return 'bottom';
    } else if(role === 'mid'){
      return 'middle'
    } else if(role === 'jg'){
      return 'jungle';
    } else if(role === 'sup'){
      return 'support'
    } else {
      return 'unknown';
    }
  }

  getLabelText(){
    if(this.showLabel){
      return this.getWholeRoleName(this.role);
    } else {
      return "Enter Champ"
    }
  }

  getRole(){
    return this.role;
  }

  getRoleEnum(){
    return (<any>Roles)[this.role]
  }

  ngOnInit() {
    console.log('init for role: ', this.role);
    this.jsonFetcher.data.subscribe((res: any) => {
      this.data = res
      for(const key of Object.keys(res)){
        this.name_list.push(key)
      }
          this.options = this.name_list;
          this.init = true
    });

    this.filteredOptions = this.myControl.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value)),
    );

  }

  private _filter(value: string): string[] {
    if(!this.init){
      return this.options;
    }
    const filterValue = value.toLowerCase();
    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }

  public getValue(){
    let selectElement = document.querySelector('input[id=' + this.role + ']') as HTMLInputElement
    return selectElement.value;
  }

  public toggleLabel(){
    this.showLabel = !this.showLabel;
  }

}
