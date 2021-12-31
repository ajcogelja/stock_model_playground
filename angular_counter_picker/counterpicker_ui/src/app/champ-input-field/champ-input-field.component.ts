import { Component, Input, OnInit, Output } from '@angular/core';
import {FormControl} from '@angular/forms';
import {Observable} from 'rxjs';
import {map, startWith} from 'rxjs/operators';
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

  updateNameVal = (e:any ) =>{
    this.name_val = e.target.value;

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

    const selectElement = document.querySelector('input')!;
    console.log('selected element:', selectElement);
    selectElement.addEventListener('input', this.updateNameVal);
    
  }

  private _filter(value: string): string[] {
    if(!this.init){
      return this.options;
    }
    const filterValue = value.toLowerCase();
    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }

  public getValue(){
    //console.log('get value', this.name_val);
    return this.name_val;
  }
}
