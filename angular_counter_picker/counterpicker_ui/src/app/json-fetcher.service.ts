import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject} from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class JsonFetcherService {

  data: BehaviorSubject<{}> = new BehaviorSubject({})
  initialized: boolean = false
  champ_data: any[string];

  constructor(private http: HttpClient) {
    this.init();

  }



  getChampData(name: string){
    if(this.champ_data){
      if(Object.keys(this.champ_data).includes(name)){
        console.log('name found in list: ', name);
        return this.champ_data[`${name}`];
      } else {
        console.log('name not found: ', name);
        return null;
      }
    } else {
      console.log('no champ data :(');
      return null;
    }
  }

  getCounters(name: string){
    if(this.champ_data){
      if(Object.keys(this.champ_data).includes(name)){
        console.log('name found in list: ', name); //need a fallback for if champ doesnt have role???
        
        const returned: any[string] = {}
          console.log('compiling all counters since role not found in list')
          Object.keys(this.champ_data[`${name}`].counters).forEach(key => {
            Object.keys(this.champ_data[`${name}`].counters[key]).forEach((champ) => {
              if(!Object.keys(returned).includes(champ)){
                returned[champ] = this.champ_data[`${name}`].counters[key][champ];
              }
            })
          })

        return returned;
      } else {
        console.log('name not found: ', name);
        return null;
      }
    } else {
      console.log('no champ data :(');
      return null;
    }
  }

  getImageSource(champName: string, width: number){
    return 'https://opgg-static.akamaized.net/images/lol/champion/' + this.getPlainName(champName) + '.png?image=c_scale,q_auto,w_' + width;
  }

  getPlainName(champName: string){
    return champName.replace('-', '').replace('.', '').replace("'", '');
  }


  getCountersForRole(name: string, role: string){
    if(this.champ_data){
      if(Object.keys(this.champ_data).includes(name)){
        console.log('name found in list: ', name); //need a fallback for if champ doesnt have role???
        if(Object.keys(this.champ_data[`${name}`].counters).includes(role)){
          return this.champ_data[`${name}`].counters[role];
        } else {
          const returned: any[string] = {}
          console.log('compiling all counters since role not found in list')
          Object.keys(this.champ_data[`${name}`].counters).forEach(key => {
            Object.keys(this.champ_data[`${name}`].counters[key]).forEach((champ) => {
              if(!Object.keys(returned).includes(champ)){
                returned[champ] = this.champ_data[`${name}`].counters[key][champ];
              }
            })
          })
          return returned;
        }
      } else {
        console.log('name not found: ', name);
        return null;
      }
    } else {
      console.log('no champ data :(');
      return null;
    }
  }

  init(){
    console.log('trying api req')
    this.getJson().subscribe(
      {
        next: (success: string) => {
          console.log('success parse: ', typeof success)
          // console.log(JSON.parse(success))
          this.data.next(success)
          this.initialized = true
          this.champ_data = (success);
          console.log('success!', success)

        },
      error: (err) => {
        console.log('err: ', err);
      },
      complete: () => {
        console.log('complete!')
      }
    })
  }

  getJson(){
    const url = 'https://s3.us-east-2.amazonaws.com/ajc.champ.bucket/champs.json'
    return this.http.get<string>(url);
  }

}
