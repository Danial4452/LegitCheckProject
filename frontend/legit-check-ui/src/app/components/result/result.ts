import { Component, OnInit, ChangeDetectorRef } from '@angular/core'; // Добавили ChangeDetectorRef
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api'; 
import { Product } from '../../models/product';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-result',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './result.html',
  styleUrl: './result.scss'
})
export class ResultComponent implements OnInit {
  product: Product | null = null;
  error: string | null = null;
  loading: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private cdr: ChangeDetectorRef // Внедряем его сюда
  ) {}

  ngOnInit() {
    const code = this.route.snapshot.paramMap.get('code');
    
    // Включаем лоадер обратно
    this.loading = true;

    setTimeout(() => {
      this.product = {
        id: 1,
        name: "Air Jordan 1 Retro High",
        brand: "Nike",
        is_authentic: true,
        serial_number: code || 'DEMO-123', 
        manufacture_location: "Vietnam, Factory PH-04",
        history: "Данная пара успешно прошла автоматизированную проверку."
      };
      
      this.loading = false; // Выключаем загрузку
      this.cdr.detectChanges(); // Принудительно обновляем экран
    }, 1500); // 1.5 секунды — идеальное время, чтобы рассмотреть лоадер
  }
}