import { TestBed } from '@angular/core/testing';

import { JsonFetcherService } from './json-fetcher.service';

describe('JsonFetcherService', () => {
  let service: JsonFetcherService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JsonFetcherService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
